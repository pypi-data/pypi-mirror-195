from typing import Any, Dict, Optional, Set

import pydantic

from classiq.interface.generator.arith import arithmetic_expression_parser
from classiq.interface.generator.arith.arithmetic_expression_template import (
    ArithmeticExpressionTemplate,
    MappingMethods,
)
from classiq.interface.generator.arith.arithmetic_result_builder import (
    ArithmeticResultBuilder,
)
from classiq.interface.generator.arith.register_user_input import RegisterUserInput

DEFAULT_TARGET_NAME = "arithmetic_target"


class Arithmetic(ArithmeticExpressionTemplate):
    output_name: str = "expression_result"
    target: Optional[RegisterUserInput] = None
    uncomputation_method: MappingMethods = MappingMethods.optimized
    inputs_to_save: Set[str] = pydantic.Field(default_factory=set)

    @pydantic.validator("target", always=True)
    def _validate_target_name(
        cls, target: Optional[RegisterUserInput]
    ) -> Optional[RegisterUserInput]:
        if target is None:
            return None
        return target if target.name else target.revalued(name=DEFAULT_TARGET_NAME)

    @pydantic.validator("inputs_to_save", always=True)
    def _validate_inputs_to_save(
        cls, inputs_to_save: Set[str], values: Dict[str, Any]
    ) -> Set[str]:
        assert all(reg in values.get("definitions", {}) for reg in inputs_to_save)
        return inputs_to_save

    def _create_ios(self) -> None:
        self._inputs = {
            name: register
            for name, register in self.definitions.items()
            if name in self._get_literal_set()
            and isinstance(register, RegisterUserInput)
        }
        self._outputs = {
            name: self._inputs[name]
            for name in self.inputs_to_save
            if name in self._inputs
        }
        self._outputs[self.output_name] = ArithmeticResultBuilder(
            graph=arithmetic_expression_parser.parse_expression(
                self.expression, validate_degrees=True
            ),
            definitions=self.definitions,
            max_fraction_places=self.max_fraction_places,
            output_name=self.output_name,
        ).result
        if self.target:
            self._inputs[self.target.name] = self.target
