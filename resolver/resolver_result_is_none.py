import random

from expression import ExpressionValidator, Expression
from operator_factory import Operator, OperatorFactory
from number_factory import NumberFactory
from number_helper import number_is_zero
from resolver.resolver_base import ExpressionResolverBase
from resolver.resolver_exceptions import (
    ExpressionResolverNotResolvable,
    ExpressionResolverMaybeNotResolvable,
)


class ResultIsNoneResolver(ExpressionResolverBase):

    def __init__(
        self,
        validator: ExpressionValidator,
        number_factory: NumberFactory,
        operator_factory: OperatorFactory,
    ):
        super().__init__(validator, number_factory, operator_factory)
        self._resolve_maximum_loop_count = 8

    def match(self, expression: Expression) -> bool:
        return expression.result is None

    def resolve(self, expression: Expression) -> Expression:
        operators = self._operators(expression)
        for _ in range(self._resolve_maximum_loop_count):
            result = self._try_resolve(expression, operators)
            if result is not None:
                return result

        raise ExpressionResolverMaybeNotResolvable(
            message=f"Try count is reached ({self._resolve_maximum_loop_count})",
            expression=expression,
        )

    def _try_resolve(
        self, expression: Expression, operators: list[Operator]
    ) -> Expression | None:
        exp_result = expression.clone()
        if exp_result.operator is None:
            try:
                exp_result.operator = next(operators)
            except StopIteration:
                raise ExpressionResolverNotResolvable(expression=expression)
        if exp_result.operator == Operator.DIV and number_is_zero(exp_result.operand2):
            return None
        if exp_result.operand1 is None:
            exp_result.operand1 = self._number_factory.next()
        if exp_result.operand2 is None:
            if not self._fill_operand2(exp_result, expression):
                return None
        exp_result.result = self._calculate(
            exp_result.operand1, exp_result.operator, exp_result.operand2
        )

        if not expression.is_match(exp_result):
            raise RuntimeError(f"Result is not match: {expression} vs {exp_result}")
        if not self._validator.validate(exp_result):
            return None
        return exp_result

    def _fill_operand2(self, exp_result: Expression, expression: Expression) -> bool:
        if exp_result.operator == Operator.SUB:
            try:
                exp_result.operand2 = self._number_factory.next(
                    maximum=exp_result.operand1
                )
            except ValueError as e:
                raise ExpressionResolverNotResolvable(expression=expression, parent=e)
        elif exp_result.operator == Operator.DIV:
            try:
                exp_result.operand2 = self._number_factory.next(
                    maximum=exp_result.operand1,
                    dividable_by=exp_result.operand1,
                    zero_allowed=False,
                )
            except ValueError as e:
                if expression.operator is None:
                    return False
                raise ExpressionResolverNotResolvable(expression=expression, parent=e)
        else:
            exp_result.operand2 = self._number_factory.next()
        return True

    def _operators(self, expression: Expression) -> list[Operator]:
        if expression.operator is not None:
            return [expression.operator]

        operators_excludes = []
        if number_is_zero(expression.operand2):
            # ?a ? 0 = c?
            # zero division not allowed
            operators_excludes.append(Operator.DIV)

        if expression.operand1 is not None and expression.operand2 is not None:
            operators_allowed = self._operator_factory.operators_weighted(
                excludes=operators_excludes
            )
            for operator in operators_allowed:
                yield operator

        # operands are empty -> all operators allowed
        yield from self._operator_factory.iter_weighted_operators(
            excludes=operators_excludes
        )
