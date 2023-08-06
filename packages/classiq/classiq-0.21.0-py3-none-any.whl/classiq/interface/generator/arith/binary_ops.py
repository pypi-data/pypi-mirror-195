from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Generic, Iterable, Optional, Tuple, TypeVar, Union

import pydantic
from pydantic.generics import GenericModel
from typing_extensions import Literal

from classiq.interface.generator.arith import number_utils
from classiq.interface.generator.arith.arithmetic_operations import (
    ArithmeticOperationParams,
    RegisterOrConst,
)
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.arith.unary_ops import Negation
from classiq.interface.generator.function_params import get_zero_input_name
from classiq.interface.generator.validations.validator_functions import (
    convert_numeric_to_fix_point_number_validator,
)

_DEFAULT_RIGHT_ARG_NAME = "right_arg"
_DEFAULT_LEFT_ARG_NAME = "left_arg"
LeftDataT = TypeVar("LeftDataT")
RightDataT = TypeVar("RightDataT")
_NumericArgumentInplaceErrorMessage = "Cannot inplace the numeric argument {}"
Numeric = (float, int)


class ArgToInplace(str, Enum):
    LEFT = "left"
    RIGHT = "right"


class BinaryOpParams(
    ArithmeticOperationParams, GenericModel, Generic[LeftDataT, RightDataT]
):
    left_arg: LeftDataT
    right_arg: RightDataT

    @pydantic.validator("left_arg")
    def _set_left_arg_name(cls, left_arg: LeftDataT) -> LeftDataT:
        if isinstance(left_arg, RegisterUserInput) and not left_arg.name:
            return left_arg.revalued(name=_DEFAULT_LEFT_ARG_NAME)  # type: ignore[return-value]
        return left_arg

    @pydantic.validator("right_arg")
    def _set_right_arg_name(cls, right_arg: RightDataT) -> RightDataT:
        if isinstance(right_arg, RegisterUserInput) and not right_arg.name:
            return right_arg.revalued(name=_DEFAULT_RIGHT_ARG_NAME)  # type: ignore[return-value]
        return right_arg

    @pydantic.root_validator(pre=True)
    def _validate_one_is_register(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        left_arg = values.get("left_arg")
        right_arg = values.get("right_arg")
        if isinstance(left_arg, Numeric) and isinstance(right_arg, Numeric):
            raise ValueError("One argument must be a register")
        if left_arg is right_arg and isinstance(left_arg, pydantic.BaseModel):
            # In case both arguments refer to the same object, copy it.
            # This prevents changes performed on one argument to affect the other.
            values["right_arg"] = left_arg.copy(deep=True)
        return values

    def _create_ios(self) -> None:
        self._inputs = dict()
        if isinstance(self.left_arg, RegisterUserInput):
            self._inputs[self.left_arg.name] = self.left_arg
        if isinstance(self.right_arg, RegisterUserInput):
            self._inputs[self.right_arg.name] = self.right_arg
        zero_input_name = get_zero_input_name(self.output_name)
        self._zero_inputs = {zero_input_name: self.result_register}
        self._outputs = {**self._inputs, **{self.output_name: self.result_register}}

    def is_inplaced(self) -> bool:
        return False

    def get_params_inplace_options(self) -> Iterable[BinaryOpParams]:
        return ()


class InplacableBinaryOpParams(BinaryOpParams, Generic[LeftDataT, RightDataT]):
    inplace_arg: Optional[ArgToInplace] = None

    @pydantic.root_validator(pre=True)
    def _validate_inplace_arg(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        left_arg = values.get("left_arg")
        right_arg = values.get("right_arg")
        inplace_arg: Optional[ArgToInplace] = values.get("inplace_arg")
        if inplace_arg == ArgToInplace.RIGHT and isinstance(right_arg, Numeric):
            raise ValueError(_NumericArgumentInplaceErrorMessage.format(right_arg))
        elif inplace_arg == ArgToInplace.LEFT and isinstance(left_arg, Numeric):
            raise ValueError(_NumericArgumentInplaceErrorMessage.format(left_arg))
        return values

    def _create_ios(self) -> None:
        BinaryOpParams._create_ios(self)
        garbage_size = self.garbage_output_size()
        if garbage_size > 0:
            self._outputs[self.garbage_output_name] = RegisterUserInput(
                name=self.garbage_output_name, size=garbage_size
            )
        if self.inplace_arg is None:
            return
        inplace_arg_name = (
            self.left_arg.name
            if self.inplace_arg == ArgToInplace.LEFT
            else self.right_arg.name
        )
        self._outputs.pop(inplace_arg_name)

        self._set_inplace_zero_inputs(inplace_arg_name, garbage_size)

    def _set_inplace_zero_inputs(
        self, inplace_arg_name: str, garbage_size: int
    ) -> None:
        self._zero_inputs.pop(get_zero_input_name(self.output_name))

        num_extra_qubits = self.outputs[self.output_name].size - (
            self._inputs[inplace_arg_name].size - garbage_size
        )
        if num_extra_qubits > 0:
            zero_input_name = get_zero_input_name(self.output_name)
            self._zero_inputs[zero_input_name] = RegisterUserInput(
                name=zero_input_name, size=num_extra_qubits
            )

    def is_inplaced(self) -> bool:
        return self.inplace_arg is not None

    def garbage_output_size(self) -> pydantic.NonNegativeInt:
        if self.inplace_arg is None:
            return 0
        arg = self.left_arg if self.inplace_arg == ArgToInplace.LEFT else self.right_arg
        return max(0, arg.integer_part_size - self.result_register.integer_part_size)

    def _carried_arguments(self) -> Tuple[Optional[LeftDataT], Optional[RightDataT]]:
        if self.inplace_arg == ArgToInplace.RIGHT and isinstance(
            self.left_arg, RegisterUserInput
        ):
            return self.left_arg, None  # type: ignore[return-value]
        elif self.inplace_arg == ArgToInplace.LEFT and isinstance(
            self.right_arg, RegisterUserInput
        ):
            return None, self.right_arg  # type: ignore[return-value]
        elif self.inplace_arg is not None:
            return None, None
        return self.left_arg, self.right_arg

    def _get_binary_op_inplace_options(self) -> Iterable[ArgToInplace]:
        right_arg = getattr(self, "right_arg", None)
        left_arg = getattr(self, "left_arg", None)
        if isinstance(right_arg, RegisterUserInput) and isinstance(
            left_arg, RegisterUserInput
        ):
            if left_arg.size > right_arg.size:
                yield ArgToInplace.LEFT
                yield ArgToInplace.RIGHT
            else:
                yield ArgToInplace.RIGHT
                yield ArgToInplace.LEFT
        elif isinstance(right_arg, RegisterUserInput):
            yield ArgToInplace.RIGHT
        elif isinstance(left_arg, RegisterUserInput):
            yield ArgToInplace.LEFT

    def get_params_inplace_options(self) -> Iterable[InplacableBinaryOpParams]:
        params_kwargs = self.copy().__dict__
        for inplace_arg in self._get_binary_op_inplace_options():
            params_kwargs["inplace_arg"] = inplace_arg
            yield self.__class__(**params_kwargs)


class BinaryOpWithIntInputs(
    BinaryOpParams[Union[int, RegisterUserInput], Union[int, RegisterUserInput]]
):
    @pydantic.root_validator()
    def validate_int_registers(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        left_arg = values.get("left_arg")
        is_left_arg_float_register = (
            isinstance(left_arg, RegisterUserInput) and left_arg.fraction_places > 0
        )
        right_arg = values.get("right_arg")
        is_right_arg_float_register = (
            isinstance(right_arg, RegisterUserInput) and right_arg.fraction_places > 0
        )
        if is_left_arg_float_register or is_right_arg_float_register:
            raise ValueError("Boolean operation are defined only for integer")
        return values

    @staticmethod
    def _is_signed(arg: Union[int, RegisterUserInput]) -> bool:
        if isinstance(arg, RegisterUserInput):
            return arg.is_signed
        return arg < 0

    def _get_result_register(self) -> RegisterUserInput:
        required_size = self._aligned_inputs_max_length()
        is_signed = self._include_sign and (
            self._is_signed(self.left_arg) or self._is_signed(self.right_arg)
        )
        return RegisterUserInput(
            size=self.output_size or required_size,
            name=self.output_name,
            is_signed=is_signed,
        )

    def _aligned_inputs_max_length(self) -> int:
        left_arg = self._arg_as_obj(self.left_arg)
        right_arg = self._arg_as_obj(self.right_arg)
        return max(
            right_arg.integer_part_size
            + int(left_arg.is_signed and not right_arg.is_signed),
            left_arg.integer_part_size
            + int(right_arg.is_signed and not left_arg.is_signed),
        )


class BinaryOpWithFloatInputs(BinaryOpParams[RegisterOrConst, RegisterOrConst]):
    _validate_args = pydantic.validator("left_arg", "right_arg", allow_reuse=True)(
        convert_numeric_to_fix_point_number_validator
    )


class BitwiseAnd(BinaryOpWithIntInputs):
    output_name: str = "bitwise_and"


class BitwiseOr(BinaryOpWithIntInputs):
    output_name: str = "bitwise_or"


class BitwiseXor(BinaryOpWithIntInputs, InplacableBinaryOpParams):
    output_name: str = "bitwise_xor"


class Adder(BinaryOpWithFloatInputs, InplacableBinaryOpParams):
    output_name: str = "sum"

    def _get_result_register(self) -> RegisterUserInput:
        arguments = tuple(
            self._arg_as_obj(arg) for arg in (self.left_arg, self.right_arg)
        )

        lb = sum(min(arg.bounds) for arg in arguments)
        ub = sum(max(arg.bounds) for arg in arguments)
        integer_part_size = number_utils.bounds_to_integer_part_size(lb, ub)

        fraction_places = max(arg.fraction_places for arg in arguments)
        size_needed = integer_part_size + fraction_places

        return RegisterUserInput(
            size=self.output_size or size_needed,
            name=self.output_name,
            fraction_places=fraction_places,
            is_signed=self._include_sign and lb < 0,
            bounds=(lb, ub) if self._include_sign else None,
        )


class Subtractor(BinaryOpWithFloatInputs, InplacableBinaryOpParams):
    output_name: str = "difference"

    def _get_result_register(self) -> RegisterUserInput:
        left_arg = self._arg_as_obj(self.left_arg)
        right_arg = self._arg_as_obj(self.right_arg)
        bounds = (
            min(left_arg.bounds) - max(right_arg.bounds),
            max(left_arg.bounds) - min(right_arg.bounds),
        )
        integer_part_size = number_utils.bounds_to_integer_part_size(*bounds)
        fraction_places = max(left_arg.fraction_places, right_arg.fraction_places)
        size_needed = integer_part_size + fraction_places
        return RegisterUserInput(
            size=self.output_size or size_needed,
            name=self.output_name,
            fraction_places=fraction_places,
            is_signed=self._include_sign and min(bounds) < 0,
            bounds=self._legal_bounds(bounds),
        )

    def garbage_output_size(self) -> pydantic.NonNegativeInt:
        if not isinstance(self.right_arg, RegisterUserInput):
            adder_params = Adder(
                left_arg=self.left_arg,
                right_arg=-self.right_arg,
                output_name=self.output_name,
                output_size=self.output_size,
                inplace_arg=self.inplace_arg,
            )
            return adder_params.garbage_output_size()

        negation_params = Negation(
            arg=self.right_arg,
            output_size=self.negation_output_size,
            inplace=self.should_inplace_negation,
        )
        negation_result = negation_params.result_register
        if self.output_size is None and max(self.right_arg.bounds) > 0:
            negation_result = negation_result.revalued(
                is_signed=True,
                bounds=(-max(self.right_arg.bounds), -min(self.right_arg.bounds)),
            )
        adder_params = Adder(
            left_arg=self.left_arg,
            right_arg=negation_result,
            output_name=self.output_name,
            output_size=self.output_size,
            inplace_arg=self.arg_to_inplace_adder,
        )
        negation_garbage_size = negation_params.garbage_output_size() * int(
            not self.should_uncompute_negation
        )
        return adder_params.garbage_output_size() + negation_garbage_size

    @property
    def should_uncompute_negation(self) -> bool:
        return self.inplace_arg == ArgToInplace.LEFT

    def _expected_negation_output_size(self) -> int:
        right_arg = self._arg_as_obj(self.right_arg)
        return right_arg.fraction_places + min(
            self.result_register.integer_part_size,
            number_utils.bounds_to_integer_part_size(
                *(-bound for bound in right_arg.bounds)
            ),
        )

    @property
    def negation_output_size(self) -> int:
        if self.output_size:
            return min(self.output_size, self._expected_negation_output_size())
        return self._expected_negation_output_size()

    @property
    def should_inplace_negation(self) -> bool:
        return self.inplace_arg is not None

    @property
    def arg_to_inplace_adder(self) -> ArgToInplace:
        return (
            ArgToInplace.LEFT
            if self.inplace_arg == ArgToInplace.LEFT
            else ArgToInplace.RIGHT
        )


class Multiplier(BinaryOpWithFloatInputs):
    output_name: str = "product"

    def _get_result_register(self) -> RegisterUserInput:
        left_arg = self._arg_as_obj(self.left_arg)
        right_arg = self._arg_as_obj(self.right_arg)
        fraction_places = left_arg.fraction_places + right_arg.fraction_places
        extremal_values = [
            left * right for left in left_arg.bounds for right in right_arg.bounds
        ]
        bounds = (min(extremal_values), max(extremal_values))
        largest_bound = max(bounds, key=abs)
        integer_places = int(largest_bound).bit_length() + int(largest_bound < 0)
        extra_sign_bit = int(
            left_arg.is_signed and right_arg.is_signed and largest_bound > 0
        )
        return RegisterUserInput(
            size=self.output_size
            or max(1, integer_places + fraction_places + extra_sign_bit),
            name=self.output_name,
            fraction_places=fraction_places,
            is_signed=self._include_sign and min(bounds) < 0,
            bounds=self._legal_bounds(bounds),
        )


class Comparator(BinaryOpWithFloatInputs):
    output_size: Literal[1] = 1

    def _get_result_register(self) -> RegisterUserInput:
        return RegisterUserInput(name=self.output_name, size=1)


class Equal(Comparator):
    output_name: str = "is_equal"


class NotEqual(Comparator):
    output_name: str = "is_not_equal"


class GreaterThan(Comparator):
    output_name: str = "is_greater_than"


class GreaterEqual(Comparator):
    output_name: str = "is_greater_equal"


class LessThan(Comparator):
    output_name: str = "is_less_than"


class LessEqual(Comparator):
    output_name: str = "is_less_equal"


class LShift(InplacableBinaryOpParams[RegisterUserInput, pydantic.NonNegativeInt]):
    output_name: str = "left_shifted"
    inplace_arg: Optional[ArgToInplace] = ArgToInplace.LEFT

    def _get_result_register(self) -> RegisterUserInput:
        new_fraction_places = max(self.left_arg.fraction_places - self.right_arg, 0)
        new_integer_part_size = self.left_arg.integer_part_size + self.right_arg
        required_size = new_integer_part_size + new_fraction_places
        return RegisterUserInput(
            size=self.output_size or required_size,
            name=self.output_name,
            is_signed=self._include_sign and self.left_arg.is_signed,
            fraction_places=new_fraction_places,
        )


class RShift(InplacableBinaryOpParams[RegisterUserInput, pydantic.NonNegativeInt]):
    output_name: str = "right_shifted"
    inplace_arg: Optional[ArgToInplace] = ArgToInplace.LEFT

    def garbage_output_size(self) -> pydantic.NonNegativeInt:
        return min(self.left_arg.size, self.right_arg) * int(
            self.inplace_arg is not None
        )

    def _get_result_register(self) -> RegisterUserInput:
        min_size: int = max(self.left_arg.size - self.right_arg, 1)
        new_fraction_places = self.left_arg.fraction_places * int(
            self.left_arg.is_signed or self.right_arg < self.left_arg.size
        )
        required_size = max(min_size, new_fraction_places)
        return RegisterUserInput(
            size=self.output_size or required_size,
            name=self.output_name,
            is_signed=self._include_sign and self.left_arg.is_signed,
            fraction_places=new_fraction_places,
        )


class CyclicShift(InplacableBinaryOpParams[RegisterUserInput, int]):
    output_name: str = "cyclic_shifted"
    inplace_arg: Optional[ArgToInplace] = ArgToInplace.LEFT

    def _get_result_register(self) -> RegisterUserInput:
        return RegisterUserInput(
            name=self.output_name,
            size=self.left_arg.size,
            is_signed=self._include_sign and self.left_arg.is_signed,
            fraction_places=self.left_arg.fraction_places,
        )
