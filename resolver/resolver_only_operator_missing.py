import random

from expression import ExpressionValidator, Expression
from operator_factory import Operator, OperatorFactory
from number_factory import NumberFactory
from number_helper import number_is_zero, number_is_equal
from resolver.resolver_base import ExpressionResolverBase
from resolver.resolver_exceptions import ExpressionResolverNotResolvable


class OnlyOperatorMissingResolver(ExpressionResolverBase):

    def __init__(
        self,
        validator: ExpressionValidator,
        number_factory: NumberFactory,
        operator_factory: OperatorFactory,
    ):
        super().__init__(validator, number_factory, operator_factory)
        self._resolve_maximum_loop_count = 8

    def match(self, expression: Expression) -> bool:
        return (
            expression.operand1 is not None
            and expression.operand2 is not None
            and expression.result is not None
            and expression.operator is None
        )

    def resolve(self, expression: Expression) -> Expression:
        operator_excludes = []
        if number_is_zero(expression.operand2):
            # zero division
            operator_excludes.append(Operator.DIV)
        operators = self._operator_factory.operators_weighted(
            excludes=operator_excludes
        )
        for operator in operators:
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
