from typing import Any, Dict, Iterable, List, Set, Tuple, Union

import pydantic

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import FunctionParams
from classiq.interface.generator.state_preparation import StatePreparation
from classiq.interface.generator.user_defined_function_params import CustomFunction

GroverStatePreparation = Union[StatePreparation, CustomFunction]


class GroverDiffuser(FunctionParams):
    variables: List[RegisterUserInput]
    state_preparation: GroverStatePreparation

    def _create_ios(self) -> None:
        self._inputs = {reg.name: reg for reg in self.variables}
        self._outputs = {reg.name: reg for reg in self.variables}

    @pydantic.validator("variables")
    def _validate_variables(
        cls, variables: List[RegisterUserInput]
    ) -> List[RegisterUserInput]:
        names = {reg.name for reg in variables}
        assert len(variables) == len(names), "Repeating names not allowed"
        return variables

    @pydantic.validator("state_preparation")
    def _validate_state_preparation(
        cls, state_preparation: GroverStatePreparation, values: Dict[str, Any]
    ) -> GroverStatePreparation:
        variables = values.get("variables", list())
        sp_inputs = state_preparation.inputs_full(assign_zero_ios=True)
        sp_outputs = state_preparation.outputs
        if len(sp_inputs) == 1 and len(sp_outputs) == 1:
            var_size = sum(reg.size for reg in variables)
            assert state_preparation.num_input_qubits(assign_zero_ios=True) == var_size
            assert state_preparation.num_output_qubits == var_size
        else:
            variable_names_and_sizes = cls._names_and_sizes(variables)
            assert cls._names_and_sizes(sp_inputs.values()) == variable_names_and_sizes
            assert cls._names_and_sizes(sp_outputs.values()) == variable_names_and_sizes
        return state_preparation

    @staticmethod
    def _names_and_sizes(
        transputs: Iterable[RegisterUserInput],
    ) -> Set[Tuple[str, int]]:
        return {(reg.name, reg.size) for reg in transputs}
