from typing import List

from classiq.interface.generator.function_call import FunctionCall
from classiq.interface.generator.function_params import IO
from classiq.interface.generator.functions import NativeFunctionDefinition
from classiq.interface.generator.parameters import ParameterMap

from classiq.model import function_handler


class FunctionGenerator(function_handler.FunctionHandler):
    def __init__(self, function_name: str) -> None:
        super().__init__()
        self._name = function_name
        self._logic_flow_list: List[FunctionCall] = list()

    @property
    def _logic_flow(self) -> List[FunctionCall]:
        return self._logic_flow_list

    def to_function_definition(self) -> NativeFunctionDefinition:
        return NativeFunctionDefinition(
            name=self._name,
            logic_flow=self._logic_flow,
            input_decls=self._custom_ios[IO.Input],
            output_decls=self._custom_ios[IO.Output],
            parameters=[
                ParameterMap(original=name, new_parameter=name)
                for name in self._parameters
            ],
        )
