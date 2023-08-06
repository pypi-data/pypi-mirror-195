from enum import Enum
from typing import Dict, Hashable, List, Set

import pydantic

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_call import FunctionCall, WireDict, WireName
from classiq.interface.generator.function_params import ArithmeticIODict, IOName
from classiq.interface.generator.functions.function_definition import FunctionDefinition
from classiq.interface.generator.parameters import ParameterFloatType, ParameterMap

LOGIC_FLOW_DUPLICATE_NAME_ERROR_MSG = (
    "Cannot have multiple function calls with the same name"
)


def _is_list_unique(lst: List[Hashable]) -> bool:
    return len(set(lst)) == len(lst)


# FIXME: temporary, until top-level logic flow is within a function definition
def update_standalone_logic_flow(
    logic_flow: List[FunctionCall], function_dict: Dict[str, FunctionDefinition]
) -> None:
    if not _is_list_unique([call.name for call in logic_flow]):
        raise ValueError(LOGIC_FLOW_DUPLICATE_NAME_ERROR_MSG)
    for fc in logic_flow:
        fc.check_and_update(function_dict)


class IOData(pydantic.BaseModel):
    wire: WireName = pydantic.Field(description="The name of the wire of the IO data.")
    reg: RegisterUserInput = pydantic.Field(
        description="The register information about the IO data."
    )

    class Config:
        frozen = True


class ClassicalType(Enum):
    Integer = "int"
    Real = "real"


class NativeFunctionDefinition(FunctionDefinition):
    """
    Facilitates the creation of a user-defined composite function

    This class sets extra to forbid so that it can be used in a Union and not "steal"
    objects from other classes.
    """

    logic_flow: List[FunctionCall] = pydantic.Field(
        default_factory=list, description="List of function calls to perform."
    )
    input_decls: Dict[IOName, IOData] = pydantic.Field(
        default_factory=dict,
        description="A mapping from the input name to the register information.",
    )
    output_decls: Dict[IOName, IOData] = pydantic.Field(
        default_factory=dict,
        description="A mapping from the output name to the register information.",
    )

    parameters: List[ParameterMap] = pydantic.Field(
        default_factory=list,
        description="The parameters (name and mapped parameter or value) of the function",
    )

    param_decls: Dict[str, ClassicalType] = pydantic.Field(default_factory=dict)

    @pydantic.validator("logic_flow")
    def _validate_logic_flow_call_names(
        cls, logic_flow: List[FunctionCall]
    ) -> List[FunctionCall]:
        function_call_names = {call.name for call in logic_flow}
        if len(function_call_names) != len(logic_flow):
            raise ValueError("Cannot have two function calls with the same name")
        return logic_flow

    def update_logic_flow(self, function_dict: Dict[str, FunctionDefinition]) -> None:
        update_standalone_logic_flow(self.logic_flow, function_dict)

    @property
    def inputs_to_wires(self) -> WireDict:
        return {name: io_data.wire for name, io_data in self.input_decls.items()}

    @property
    def outputs_to_wires(self) -> WireDict:
        return {name: io_data.wire for name, io_data in self.output_decls.items()}

    @property
    def inputs(self) -> ArithmeticIODict:
        return {name: io_data.reg for name, io_data in self.input_decls.items()}

    @property
    def outputs(self) -> ArithmeticIODict:
        return {name: io_data.reg for name, io_data in self.output_decls.items()}

    @property
    def input_set(self) -> Set[IOName]:
        return set(self.inputs_to_wires.keys())

    @property
    def output_set(self) -> Set[IOName]:
        return set(self.outputs_to_wires.keys())

    @property
    def parameters_mapping(self) -> Dict[str, ParameterFloatType]:
        return {
            parameter.original: parameter.new_parameter for parameter in self.parameters
        }
