import abc
from typing import List, Optional

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import ArithmeticIODict, FunctionParams


class OracleTemplate(abc.ABC, FunctionParams):
    def get_power_order(self) -> Optional[int]:
        return 2

    @abc.abstractmethod
    def _get_register_transputs(self) -> ArithmeticIODict:
        pass

    def _create_ios(self) -> None:
        self._inputs = self._get_register_transputs()
        self._outputs = {**self._inputs}

    def variables(self) -> List[RegisterUserInput]:
        return list(self._inputs.values())
