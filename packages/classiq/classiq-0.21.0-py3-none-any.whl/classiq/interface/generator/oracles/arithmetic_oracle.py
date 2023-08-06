import ast

import pydantic

from classiq.interface.generator.arith.arithmetic import Arithmetic
from classiq.interface.generator.arith.arithmetic_expression_template import (
    ArithmeticExpressionTemplate,
    UncomputationMethods,
)
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.oracles.oracle_template import (
    ArithmeticIODict,
    OracleTemplate,
)

_ARITHMETIC_EXPRESSION_RESULT_NAME: str = "expression_result"


class ArithmeticOracle(OracleTemplate, ArithmeticExpressionTemplate):
    uncomputation_method: UncomputationMethods = UncomputationMethods.optimized

    @pydantic.validator("expression")
    def _validate_compare_expression(cls, expression: str) -> str:
        ast_obj = ast.parse(expression, "", "eval")
        if not isinstance(ast_obj, ast.Expression):
            raise ValueError("Must be an expression")
        if not isinstance(ast_obj.body, (ast.Compare, ast.BoolOp)):
            raise ValueError("Must be a comparison expression")
        return expression

    def get_arithmetic_expression_params(self) -> Arithmetic:
        return Arithmetic(
            max_fraction_places=self.max_fraction_places,
            expression=self.expression,
            definitions=self.definitions,
            uncomputation_method=self.uncomputation_method,
            qubit_count=self.qubit_count,
            simplify=self.simplify,
            output_name=_ARITHMETIC_EXPRESSION_RESULT_NAME,
            target=RegisterUserInput(size=1),
            inputs_to_save=set(self.definitions.keys()),
        )

    def _get_register_transputs(self) -> ArithmeticIODict:
        return {
            name: register
            for name, register in self.definitions.items()
            if name in self._get_literal_set()
            and isinstance(register, RegisterUserInput)
        }
