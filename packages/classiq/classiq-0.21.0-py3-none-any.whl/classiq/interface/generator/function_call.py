from __future__ import annotations

import functools
import itertools
import random
import re
import string
from collections import defaultdict
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    Match,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import pydantic
from pydantic import BaseModel
from sympy import Expr, sympify

from classiq.interface.generator import function_param_list, function_params as f_params
from classiq.interface.generator.arith.arithmetic import Arithmetic
from classiq.interface.generator.control_state import ControlState
from classiq.interface.generator.expressions import Expression
from classiq.interface.generator.function_params import (
    IO,
    NAME_REGEX,
    ArithmeticIODict,
    FunctionParams,
    IOName,
    validate_expression_str,
)
from classiq.interface.generator.functions import FunctionDefinition
from classiq.interface.generator.functions.foreign_function_definition import (
    ForeignFunctionDefinition,
)
from classiq.interface.generator.mcx import Mcx
from classiq.interface.generator.partitioned_register import (
    PartitionedRegister,
    RegisterPartition,
    slices_to_partitions_with_payload,
)
from classiq.interface.generator.slice_parsing_utils import (
    IO_REGEX,
    NAME,
    SEPARATOR,
    SLICING,
    parse_io_slicing,
)
from classiq.interface.generator.user_defined_function_params import CustomFunction
from classiq.interface.helpers.custom_pydantic_types import PydanticNonEmptyString

from classiq import RegisterUserInput
from classiq.exceptions import ClassiqControlError, ClassiqValueError

DEFAULT_SUFFIX_LEN: int = 6
BAD_INPUT_ERROR_MSG = "Bad input name given"
BAD_OUTPUT_ERROR_MSG = "Bad output name given"
BAD_INPUT_EXPRESSION_MSG = "Bad input expression given"
BAD_OUTPUT_EXPRESSION_MSG = "Bad output expression given"
BAD_INPUT_SLICING_MSG = "Bad input slicing / indexing given"
BAD_OUTPUT_SLICING_MSG = "Bad output slicing / indexing given"
BAD_CALL_NAME_ERROR_MSG = "Call name must be in snake_case and begin with a letter"
CUSTOM_FUNCTION_SINGLE_IO_ERROR = (
    "Custom function currently supports explicit IO specification only via dictionary"
)

LEGAL_SLICING = rf"(\-?\d+)?({SEPARATOR}(\-?\d+)?)?({SEPARATOR}(\-?\d+)?)?"

_ALPHANUM_CHARACTERS = string.ascii_letters + string.digits

RegNameAndSlice = Tuple[str, slice]
ParsedIOs = Iterable[Tuple[str, slice, str]]

ZERO_INDICATOR = "0"
INVERSE_SUFFIX = "_qinverse"

SUFFIX_MARKER = "cs4id"

WireName = PydanticNonEmptyString
WireDict = Dict[IOName, WireName]
IOType = Union[WireDict, WireName]
PartitionToWireName = Mapping[RegisterPartition, WireName]

SUFFIX_RANDOMIZER = random.Random()


def randomize_suffix(suffix_len: int = DEFAULT_SUFFIX_LEN) -> str:
    return "".join(
        SUFFIX_RANDOMIZER.choice(_ALPHANUM_CHARACTERS)
        for _ in range(suffix_len)  # nosec B311
    )


class FunctionCall(BaseModel):
    function: str = pydantic.Field(description="The function that is called")
    function_params: f_params.FunctionParams = pydantic.Field(
        description="The parameters necessary for defining the function"
    )

    params: Dict[str, Expression] = pydantic.Field(default_factory=dict)

    is_inverse: bool = pydantic.Field(
        default=False, description="Call the function inverse."
    )

    assign_zero_ios: bool = pydantic.Field(
        default=False,
        description="Assign zero inputs/outputs to pre-defined registers",
    )

    release_by_inverse: bool = pydantic.Field(
        default=False, description="Release zero inputs in inverse call."
    )
    control_states: List[ControlState] = pydantic.Field(
        default_factory=list,
        description="Call the controlled function with the given controlled states.",
    )
    should_control: bool = pydantic.Field(
        default=True,
        description="False value indicates this call shouldn't be controlled even if the flow is controlled.",
    )
    inputs: IOType = pydantic.Field(
        default_factory=dict,
        description="A mapping from the input name to the wire it connects to",
    )
    outputs: IOType = pydantic.Field(
        default_factory=dict,
        description="A mapping from the output name to the wire it connects to",
    )
    power: pydantic.NonNegativeInt = pydantic.Field(
        default=1, description="Number of successive calls to the operation"
    )

    name: PydanticNonEmptyString = pydantic.Field(
        default=None,
        description="The name of the function instance. "
        "If not set, determined automatically.",
    )

    _non_zero_input_wires: List[WireName] = pydantic.PrivateAttr(default_factory=list)
    _non_zero_output_wires: List[WireName] = pydantic.PrivateAttr(default_factory=list)

    _partitioned_inputs: List[PartitionedRegister] = pydantic.PrivateAttr(
        default_factory=list
    )
    _partitioned_outputs: List[PartitionedRegister] = pydantic.PrivateAttr(
        default_factory=list
    )
    _input_partition_wirename_map: PartitionToWireName = pydantic.PrivateAttr(
        default_factory=dict
    )
    _output_partition_wirename_map: PartitionToWireName = pydantic.PrivateAttr(
        default_factory=dict
    )

    _func_def: Optional[FunctionDefinition] = pydantic.PrivateAttr(default=None)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._non_zero_input_wires = self._non_zero_wires(self.inputs_dict.values())
        self._non_zero_output_wires = self._non_zero_wires(self.outputs_dict.values())

    @property
    def func_def(self) -> Optional[FunctionDefinition]:
        return self._func_def

    # FIXME: setter decorator doesn't work here - why?
    def set_func_def(self, fd: Optional[FunctionDefinition]) -> None:
        self._func_def = fd

    def __eq__(self, other) -> bool:
        return isinstance(other, FunctionCall) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    @property
    def non_zero_input_wires(self) -> List[WireName]:
        return self._non_zero_input_wires

    @property
    def non_zero_output_wires(self) -> List[WireName]:
        return self._non_zero_output_wires

    @property
    def inputs_dict(self) -> WireDict:
        assert isinstance(self.inputs, dict)
        return self.inputs

    @property
    def outputs_dict(self) -> WireDict:
        assert isinstance(self.outputs, dict)
        return self.outputs

    @property
    def input_regs_dict(self) -> ArithmeticIODict:
        ctrl_regs_dict = {
            ctrl_state.name: ctrl_state.control_register
            for ctrl_state in self.control_states
        }
        return {
            **self._true_io_dict(io=IO.Input),
            **ctrl_regs_dict,
        }

    @property
    def output_regs_dict(self) -> ArithmeticIODict:
        ctrl_regs_dict = {
            ctrl_state.name: ctrl_state.control_register
            for ctrl_state in self.control_states
        }
        return {
            **self._true_io_dict(io=IO.Output),
            **ctrl_regs_dict,
        }

    def _true_io_dict(self, io: IO) -> ArithmeticIODict:
        if (io == IO.Input) != self.is_inverse:
            return self.function_params.inputs_full(self.assign_zero_ios)
        return self.function_params.outputs

    @pydantic.validator("name", pre=True, always=True)
    def _create_name(cls, name: Optional[str], values: Dict[str, Any]) -> str:
        """
        generates a name to a user defined-functions as follows:
        <function_name>_<SUFFIX_MARKER>_<random_suffix>
        """
        if name is not None:
            match = re.fullmatch(pattern=NAME_REGEX, string=name)
            if match is None:
                raise ValueError(BAD_CALL_NAME_ERROR_MSG)
            return name

        function = values.get("function")
        params = values.get("function_params")
        suffix = f"{SUFFIX_MARKER}_{randomize_suffix()}"
        if not function or params is None:
            return name if name else suffix
        return f"{function}_{suffix}"

    @pydantic.root_validator(pre=True)
    def validate_composite_name(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(values.get("unitary_params"), CustomFunction) and not values.get(
            "unitary"
        ):
            raise ClassiqValueError(
                "`PhaseEstimation` of a user define function (`CustomFunction`) must receive the function name from the `unitary` field"
            )
        return values

    @pydantic.root_validator(pre=True)
    def _parse_function_params(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        f_params.parse_function_params_values(
            values=values,
            params_key="function_params",
            discriminator_key="function",
            param_classes=function_param_list.function_param_library.param_list,
            default_parser_class=CustomFunction,
        )
        return values

    # TODO: note that this checks FunctionCall input register names
    # are PARTIAL to FunctionParams input register names, not EQUAL.
    # We might want to change that.
    @staticmethod
    def _validate_input_names(
        *,
        params: f_params.FunctionParams,
        inputs: WireDict,
        is_inverse: bool,
        control_states: List[ControlState],
        assign_zero_ios: bool,
    ) -> None:
        (
            invalid_expressions,
            invalid_slicings,
            invalid_names,
        ) = FunctionCall._get_invalid_ios(
            expressions=inputs.keys(),
            params=params,
            io=f_params.input_io(is_inverse),
            control_states=control_states,
            assign_zero_ios=assign_zero_ios,
        )
        error_msg = []
        if invalid_expressions:
            error_msg.append(f"{BAD_INPUT_EXPRESSION_MSG}: {invalid_expressions}")
        if invalid_names:
            error_msg.append(f"{BAD_INPUT_ERROR_MSG}: {invalid_names}")
        if invalid_slicings:
            error_msg.append(f"{BAD_INPUT_SLICING_MSG}: {invalid_slicings}")
        if error_msg:
            raise ValueError("\n".join(error_msg))

    def _check_params_against_declaration(self) -> None:
        if self.func_def is None or isinstance(
            self.func_def, ForeignFunctionDefinition
        ):
            return
        param_decls = self.func_def.param_decls  # type:ignore[attr-defined]
        unknown_params = self.params.keys() - param_decls.keys()
        if unknown_params:
            raise ValueError(
                f"Unknown parameters {unknown_params} in call to '{self.func_def.name}'."
            )

        missing_params = param_decls.keys() - self.params.keys()
        if missing_params:
            raise ValueError(
                f"Missing parameters {missing_params} in call to '{self.func_def.name}'."
            )

    def _resolve_function_def(self, function_dict: Dict[str, FunctionDefinition]):
        if self.function not in function_dict:
            raise ValueError("The function is not found in included library.")
        self.set_func_def(function_dict[self.function])
        self._check_params_against_declaration()

    def check_and_update(self, function_dict: Dict[str, FunctionDefinition]) -> None:
        if not isinstance(self.function_params, CustomFunction):
            return
        self._resolve_function_def(function_dict)
        assert self.func_def is not None
        self.function_params.generate_ios(
            inputs=self.func_def.inputs,
            outputs=self.func_def.outputs,
        )
        self._validate_custom_function_io()

    @pydantic.validator("params", pre=True)
    def validate_parameters(cls, params: Dict[str, str]) -> Dict[str, str]:
        for name, expr in params.items():
            if type(expr) == str:
                validate_expression_str(name, expr)
        return params

    @pydantic.validator("assign_zero_ios")
    def _validate_arithmetic_cannot_assign_zero_ios(
        cls, assign_zero_ios: bool, values: Dict[str, Any]
    ) -> bool:
        assert not (
            values.get("function") == Arithmetic.discriminator() and assign_zero_ios
        ), "when using the Arithmetic function, assign to the expression result register via the target parameter instead of the assign_zero_ios flag"
        return assign_zero_ios

    @pydantic.validator("control_states")
    def _validate_control_states(
        cls, control_states: List[ControlState], values: Dict[str, Any]
    ) -> List[ControlState]:
        control_names = [ctrl_state.name for ctrl_state in control_states]
        function_params = values.get("function_params")
        assign_zero_ios = values.get("assign_zero_ios")
        if not (
            isinstance(function_params, FunctionParams)
            and isinstance(assign_zero_ios, bool)
        ):
            return control_states
        all_input_names = [
            *function_params.inputs_full(assign_zero_ios=assign_zero_ios),
            *control_names,
        ]
        all_output_names = [*function_params.outputs, *control_names]
        if any(
            cls._has_repetitions(name_list)
            for name_list in (control_names, all_input_names, all_output_names)
        ):
            raise ClassiqControlError()
        return control_states

    @staticmethod
    def _has_repetitions(name_list: Sequence[str]) -> bool:
        return len(set(name_list)) < len(name_list)

    @staticmethod
    def _validate_slices(
        io: IO,
        inputs: IOType,
        fp: FunctionParams,
        assign_zero_ios: bool,
        control_states: List[ControlState],
    ) -> None:
        name_slice_pairs = [parse_io_slicing(input) for input in inputs]
        slices_dict: Dict[str, List[slice]] = defaultdict(list)
        for name, slice in name_slice_pairs:
            slices_dict[name].append(slice)

        fp_inputs = fp.inputs_full(assign_zero_ios) if (io == IO.Input) else fp.outputs
        widths = {name: reg.size for name, reg in fp_inputs.items()}
        control_names = {state.name for state in control_states}

        for name in slices_dict:
            if name in control_names:
                continue
            assert name in widths, "Name not in widths"
            if not FunctionCall._register_validate_slices(
                slices_dict[name], widths[name]
            ):
                raise ValueError(BAD_INPUT_SLICING_MSG)

    def partitioned_io_map(self, io: IO) -> PartitionToWireName:
        if not self._partitioned_inputs:
            self._calculate_partition_data()
        if io == IO.Input:
            return self._input_partition_wirename_map
        return self._output_partition_wirename_map

    def partitioned_io(self, io: IO) -> Sequence[PartitionedRegister]:
        if not self._partitioned_inputs:
            self._calculate_partition_data()
        if io == IO.Input:
            return self._partitioned_inputs
        return self._partitioned_outputs

    def _calculate_partition_data(self) -> None:
        input_params_ios = self._params_ios(IO.Input)
        input_io_dict = self.inputs_dict
        (
            self._partitioned_inputs,
            self._input_partition_wirename_map,
        ) = FunctionCall._partition_registers(input_io_dict, input_params_ios)

        output_params_ios = self._params_ios(IO.Output)
        output_io_dict = self.outputs_dict
        (
            self._partitioned_outputs,
            self._output_partition_wirename_map,
        ) = FunctionCall._partition_registers(output_io_dict, output_params_ios)

    def _params_ios(self, io: IO) -> Dict[IOName, RegisterUserInput]:
        params_ios = {
            state.name: state.control_register for state in self.control_states
        }
        params_ios.update(
            self.function_params.inputs_full(self.assign_zero_ios)
            if (io == IO.Input) != self.is_inverse
            else self.function_params.outputs
        )
        return params_ios

    @staticmethod
    def _partition_registers(
        io_dict: Dict[IOName, WireName],
        params_ios: Dict[IOName, RegisterUserInput],
    ) -> Tuple[List[PartitionedRegister], PartitionToWireName]:
        parsed_io_sequence: List[Tuple[IOName, slice, WireName]] = []

        for io_name, wire_name in io_dict.items():
            io_name, slice_ = parse_io_slicing(io_name)
            parsed_io_sequence.append((io_name, slice_, wire_name))

        slices_dict: Dict[
            IOName, List[Tuple[slice, Tuple[WireName, int]]]
        ] = defaultdict(list)

        # We keep track of the index so that we can put the slices in the same order as the io_dict
        for index, (io_name, slice_, wire_name) in enumerate(parsed_io_sequence):
            slices_dict[io_name].append((slice_, (wire_name, index)))

        names_to_ranges = {name: range(reg.size) for name, reg in params_ios.items()}

        if not (set(slices_dict.keys()).issubset(set(names_to_ranges))):
            raise ValueError("Slice without corresponding range")

        partitioned_register_by_index: Dict[
            int, Tuple[RegisterPartition, WireName]
        ] = dict()

        all_partitioned_registers = []

        for name, slice_wire_tuples in slices_dict.items():
            reg_range = names_to_ranges[name]
            partition_payload_pairs = slices_to_partitions_with_payload(
                name, reg_range, slice_wire_tuples
            )
            for partition, (wire_name, index) in partition_payload_pairs:
                partitioned_register_by_index[index] = (partition, wire_name)
            all_partitioned_registers.append(
                partition_payload_pairs[0][0].partitioned_register
            )

        # Reorder the partitions
        partition_wire_list = []
        for index in range(len(parsed_io_sequence)):
            partition_wire_list.append(partitioned_register_by_index[index])

        return all_partitioned_registers, dict(partition_wire_list)

    @staticmethod
    def _register_validate_slices(slices: List[slice], reg_width: int) -> bool:
        widths_separated = [len(range(reg_width)[reg_slice]) for reg_slice in slices]
        # examples: slice(0), slice(5,None) when width <= 5, slice(5,3)
        empty_slices = 0 in widths_separated

        max_stop = max(reg_slice.stop or 0 for reg_slice in slices)
        out_of_range = max_stop > reg_width

        all_widths_separated = sum(widths_separated)
        all_indices = set(
            itertools.chain.from_iterable(
                range(reg_width)[reg_slice] for reg_slice in slices
            )
        )
        all_widths_combined = len(all_indices)
        overlapping_slices = all_widths_combined != all_widths_separated

        return not any((empty_slices, out_of_range, overlapping_slices))

    @pydantic.validator("inputs")
    def _validate_inputs(cls, inputs: IOType, values: Dict[str, Any]) -> WireDict:
        params: Optional[FunctionParams] = values.get("function_params")
        is_inverse: bool = values.get("is_inverse", False)
        assign_zero_ios: bool = values.get("assign_zero_ios", False)
        control_states: List[ControlState] = values.get("control_states", list())
        if params is None:
            return dict()
        if isinstance(params, CustomFunction):
            if not isinstance(inputs, dict):
                raise ValueError(CUSTOM_FUNCTION_SINGLE_IO_ERROR)
            return inputs

        if isinstance(inputs, str):
            inputs = FunctionCall._single_wire_to_dict(
                io=f_params.IO.Input,
                is_inverse=is_inverse,
                io_wire=inputs,
                params=params,
                assign_zero_ios=assign_zero_ios,
            )

        cls._validate_input_names(
            params=params,
            inputs=inputs,
            is_inverse=is_inverse,
            control_states=control_states,
            assign_zero_ios=assign_zero_ios,
        )

        cls._validate_slices(
            IO(not is_inverse), inputs, params, assign_zero_ios, control_states
        )

        return inputs

    @staticmethod
    def _validate_output_names(
        *,
        params: f_params.FunctionParams,
        outputs: WireDict,
        is_inverse: bool,
        control_states: List[ControlState],
        assign_zero_ios: bool,
    ) -> None:
        (
            invalid_expressions,
            invalid_slicings,
            invalid_names,
        ) = FunctionCall._get_invalid_ios(
            expressions=outputs.keys(),
            params=params,
            io=f_params.output_io(is_inverse),
            control_states=control_states,
            assign_zero_ios=assign_zero_ios,
        )
        error_msg = []
        if invalid_expressions:
            error_msg.append(f"{BAD_OUTPUT_EXPRESSION_MSG}: {invalid_expressions}")
        if invalid_names:
            error_msg.append(f"{BAD_OUTPUT_ERROR_MSG}: {invalid_names}")
        if invalid_slicings:
            error_msg.append(f"{BAD_OUTPUT_SLICING_MSG}: {invalid_slicings}")
        if error_msg:
            raise ValueError("\n".join(error_msg))

    @pydantic.validator("outputs")
    def _validate_outputs(cls, outputs: IOType, values: Dict[str, Any]) -> IOType:
        params = values.get("function_params")
        is_inverse: bool = values.get("is_inverse", False)
        assign_zero_ios: bool = values.get("assign_zero_ios", False)
        control_states = values.get("control_states", list())
        if params is None:
            return outputs
        if isinstance(params, CustomFunction):
            if not isinstance(outputs, dict):
                raise ValueError(CUSTOM_FUNCTION_SINGLE_IO_ERROR)
            return outputs

        if isinstance(outputs, str):
            outputs = FunctionCall._single_wire_to_dict(
                io=f_params.IO.Output,
                is_inverse=is_inverse,
                io_wire=outputs,
                params=params,
                assign_zero_ios=assign_zero_ios,
            )

        cls._validate_output_names(
            params=params,
            outputs=outputs,
            is_inverse=is_inverse,
            control_states=control_states,
            assign_zero_ios=assign_zero_ios,
        )

        cls._validate_slices(
            IO(is_inverse), outputs, params, assign_zero_ios, control_states
        )

        return outputs

    @pydantic.validator("power", always=True)
    def _validate_power(
        cls, power: pydantic.NonNegativeInt, values: Dict[str, Any]
    ) -> pydantic.NonNegativeInt:
        function_params = values.get("function_params")
        if function_params is None:
            return power
        if power != 1 and not function_params.is_powerable(
            values.get("assign_zero_ios")
        ):
            raise ValueError("Cannot power this operator")
        return power

    @staticmethod
    def _single_wire_to_dict(
        io: f_params.IO,
        is_inverse: bool,
        io_wire: WireName,
        params: f_params.FunctionParams,
        assign_zero_ios: bool = False,
    ) -> WireDict:
        params_io = list(
            params.inputs_full(assign_zero_ios)
            if (io == IO.Input) != is_inverse
            else params.outputs
        )

        if len(params_io) == 1:
            return {list(params_io)[0]: io_wire}
        error_message = _generate_single_io_err(
            io_str=io.name.lower(),
            io_regs=params_io,
            io_wire=io_wire,
            function_name=type(params).__name__,
        )
        raise ValueError(error_message)

    @staticmethod
    def _get_invalid_ios(
        *,
        expressions: Iterable[str],
        params: f_params.FunctionParams,
        io: f_params.IO,
        control_states: List[ControlState],
        assign_zero_ios: bool,
    ) -> Tuple[List[str], List[str], List[str]]:
        expression_matches: Iterable[Optional[Match]] = map(
            functools.partial(re.fullmatch, IO_REGEX), expressions
        )

        valid_matches: List[Match] = []
        invalid_expressions: List[str] = []
        for expression, expression_match in zip(expressions, expression_matches):
            invalid_expressions.append(
                expression
            ) if expression_match is None else valid_matches.append(expression_match)

        invalid_slicings: List[str] = []
        invalid_names: List[str] = []
        valid_names = frozenset(
            params.inputs_full(assign_zero_ios) if io == IO.Input else params.outputs
        )
        for match in valid_matches:
            name = match.groupdict().get(NAME)
            if name is None:
                raise AssertionError("Input/output name validation error")

            slicing = match.groupdict().get(SLICING)
            if slicing is not None and re.fullmatch(LEGAL_SLICING, slicing) is None:
                invalid_slicings.append(match.string)

            if name in valid_names:
                continue
            elif all(state.name != name for state in control_states):
                invalid_names.append(name)

        return invalid_expressions, invalid_slicings, invalid_names

    def _validate_custom_function_io(self) -> None:
        if not isinstance(self.function_params, CustomFunction):
            raise AssertionError("CustomFunction object expected.")
        FunctionCall._validate_input_names(
            params=self.function_params,
            inputs=self.inputs_dict,
            is_inverse=self.is_inverse,
            control_states=self.control_states,
            assign_zero_ios=self.assign_zero_ios,
        )
        FunctionCall._validate_output_names(
            params=self.function_params,
            outputs=self.outputs_dict,
            is_inverse=self.is_inverse,
            control_states=self.control_states,
            assign_zero_ios=self.assign_zero_ios,
        )

    def parse_inputs(self) -> ParsedIOs:
        reg_names_and_slices = zip(*map(parse_io_slicing, self.inputs_dict.keys()))
        wire_names = self.inputs_dict.values()
        # types cannot be resolved from zip
        return zip(*reg_names_and_slices, wire_names)  # type: ignore[return-value]

    def parse_outputs(self) -> ParsedIOs:
        reg_names_and_slices = zip(*map(parse_io_slicing, self.outputs_dict.keys()))
        wire_names = self.outputs_dict.values()
        # types cannot be resolved from zip
        return zip(*reg_names_and_slices, wire_names)  # type: ignore[return-value]

    def get_param_exprs(self) -> Dict[str, Expr]:
        if isinstance(self.function_params, CustomFunction):
            return {
                name: sympify(expr_obj.expr) for name, expr_obj in self.params.items()
            }
        else:
            return {
                name: sympify(raw_expr)
                for name, raw_expr in self.function_params
                if self.function_params.is_field_gen_param(name)
            }

    def subs_params(self, context_params: Dict[str, Expr]) -> Dict[str, Expr]:
        res = dict()
        for param_name, param_expr in self.get_param_exprs().items():
            for sym, expr in context_params.items():
                param_expr = param_expr.subs(sym, expr)
            res[param_name] = param_expr
        return res

    @staticmethod
    def _non_zero_wires(wires: Iterable[WireName]) -> List[WireName]:
        return [wire for wire in wires if wire != ZERO_INDICATOR]

    def modified_copy(
        self,
        *,
        wire_prefix: str,
        outer_release_by_inverse: bool,
        outer_should_control: bool,
    ) -> FunctionCall:
        call_kwargs = self.__dict__.copy()
        call_kwargs["release_by_inverse"] = (
            self.release_by_inverse or outer_release_by_inverse
        )
        call_kwargs["should_control"] = self.should_control and outer_should_control
        call_kwargs["inputs"] = add_prefix_to_wire_dict(self.inputs_dict, wire_prefix)
        call_kwargs["outputs"] = add_prefix_to_wire_dict(self.outputs_dict, wire_prefix)
        return FunctionCall(**call_kwargs)

    def inverse(self) -> FunctionCall:
        call_kwargs = self.__dict__.copy()
        call_kwargs["inputs"] = self.outputs_dict
        call_kwargs["outputs"] = self.inputs_dict
        call_kwargs["name"] = self._inverse_name(self.name)
        call_kwargs["is_inverse"] = not self.is_inverse
        return FunctionCall(**call_kwargs)

    @staticmethod
    def _inverse_name(name: str):
        if name.endswith(INVERSE_SUFFIX):
            return name[: -len(INVERSE_SUFFIX)]
        return f"{name}{INVERSE_SUFFIX}"

    def can_extend_control(self) -> bool:
        return self.should_control and (
            bool(self.control_states) or type(self.function_params) == Mcx
        )

    def control(
        self, control_state: ControlState, input_wire: WireName, output_wire: WireName
    ) -> FunctionCall:
        if (
            control_state.name in self.inputs_dict
            or control_state.name in self.outputs_dict
        ):
            raise ValueError(f"Control name: {control_state.name} already exists")

        inputs, outputs = self.inputs_dict.copy(), self.outputs_dict.copy()
        inputs.update({control_state.name: input_wire})
        outputs.update({control_state.name: output_wire})

        call_kwargs = self.__dict__.copy()
        call_kwargs["inputs"] = inputs
        call_kwargs["outputs"] = outputs
        call_kwargs["name"] = f"{self.name}_{control_state.name}"
        call_kwargs["control_states"] = self.control_states + [control_state]
        return FunctionCall(**call_kwargs)


def add_prefix_to_wire_dict(wire_dict: WireDict, prefix: str) -> WireDict:
    def _prefix_wire(wire_name: WireName) -> WireName:
        if wire_name == ZERO_INDICATOR:
            return ZERO_INDICATOR
        return prefix + wire_name

    return {
        io_name: _prefix_wire(wire_name) for io_name, wire_name in wire_dict.items()
    }


def _generate_single_io_err(
    *, io_str: str, io_regs: Iterable[str], io_wire: str, function_name: str
) -> str:
    if not io_regs:
        return (
            f'Cannot create {io_str} wire "{io_wire}". '
            f"Function {function_name} has no {io_str} registers."
        )

    return (
        f"Cannot use a single {io_str} wire. "
        f"Function {function_name} has multiple {io_str} registers: {io_regs}."
    )
