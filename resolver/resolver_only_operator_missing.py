import random

from expression import ExpressionValidator, Expression, Operator
from number_factory import NumberFactory
from number_helper import number_is_zero, number_is_equal
from resolver.resolver_base import ExpressionResolverBase
from resolver.resolver_exceptions import ExpressionResolverNotResolvable


class OnlyOperatorMissingResolver(ExpressionResolverBase):

    def __init__(self, validator: ExpressionValidator, number_factory: NumberFactory):
        super().__init__(validator, number_factory)
        self._resolve_maximum_loop_count = 8

    def match(self, expression: Expression) -> bool:
        return (
            expression.operand1 is not None
            and expression.operand2 is not None
            and expression.result is not None
            and expression.operator is None
        )

    def resolve(self, expression: Expression) -> Expression:
        operators = Operator.get_operators_without_eq()
        random.shuffle(operators)
        for operator in operators:
            if operator == Operator.DIV and number_is_zero(expression.operand2):
                # zero division
                continue
            exp_result = expression.clone()
            exp_result.operator = operator
            exp_result.result = self._calculate(
                exp_result.operand1, operator, exp_result.operand2
            )

            if not number_is_equal(exp_result.result, expression.result):
                continue

            if not expression.is_match(exp_result):
                raise RuntimeError(f"Result is not match: {expression} vs {exp_result}")
            if not self._validator.validate(exp_result):
                continue
            return exp_result
        raise ExpressionResolverNotResolvable(expression=expression)
