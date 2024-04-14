import random

from expression import ExpressionValidator, Expression, Operator, is_zero_division
from number_factory import NumberFactory
from resolver.resolver_base import ExpressionResolverBase
from resolver.resolver_exceptions import (
    ExpressionResolverMaybeNotResolvable,
    ExpressionResolverNotResolvable,
)


class ResultIsAvailableResolver(ExpressionResolverBase):

    def __init__(self, validator: ExpressionValidator, number_factory: NumberFactory):
        super().__init__(validator, number_factory)
        self._resolve_maximum_loop_count = 8

    def match(self, expression: Expression) -> bool:
        return expression.result is not None

    def resolve(self, expression: Expression) -> Expression:
        for _ in range(self._resolve_maximum_loop_count):
            result = self._try_resolve(expression)
            if result is not None:
                return result

        raise ExpressionResolverMaybeNotResolvable(
            message=f"Try count is reached ({self._resolve_maximum_loop_count})",
            expression=expression,
        )

    def _try_resolve(self, expression: Expression) -> Expression | None:
        exp_calc = expression.clone()
        exp_result = expression.clone()
        operator = (
            expression.operator
            if expression.operator is not None
            else random.choice(Operator.get_operators_without_eq())
        )
        if exp_result.operator is None:
            exp_result.operator = operator
        operands_is_empty = exp_calc.operand1 is None and exp_calc.operand2 is None
        if operands_is_empty:
            exp_result.operand1 = exp_calc.operand1 = self._number_factory.next()

        # branches by operator
        if operator == Operator.ADD:
            ResultIsAvailableResolver._resolve_add(exp_calc)
        elif operator == Operator.SUB:
            ResultIsAvailableResolver._resolve_sub(exp_calc, exp_result)
        elif operator == Operator.MUL:
            if not self._resolve_mul(
                exp_calc, exp_result, operands_is_empty, expression
            ):
                return None
        elif operator == Operator.DIV:
            self._resolve_div(exp_calc, exp_result, operands_is_empty)
        else:
            raise RuntimeError(f"Invalid operator: {operator}")

        if not self._calculate_result(exp_calc, exp_result):
            return None

        if not expression.is_match(exp_result):
            raise RuntimeError(f"Result is not match: {expression} vs {exp_result}")
        if not self._validator.validate(exp_result):
            return None
        return exp_result

    @staticmethod
    def _resolve_add(exp_calc: Expression):
        # a + b = c
        # a + ? = c -> c - a = b
        # ? + b = c -> c - b = a
        exp_calc.operator = Operator.SUB

    @staticmethod
    def _resolve_sub(exp_calc: Expression, exp_result: Expression):
        # a - b = c
        if exp_result.operand1 is None:
            # ? - b = c -> c + b = a
            exp_calc.operator = Operator.ADD
            return
        #  a - ? = c -> a - c = b
        exp_calc.operator = Operator.SUB
        _tmp = exp_calc.operand1
        exp_calc.operand1 = exp_calc.result
        exp_calc.result = _tmp

    def _resolve_div(
        self, exp_calc: Expression, exp_result: Expression, operands_is_empty: bool
    ):
        # a / b = c
        if operands_is_empty:
            # make the simplest case with multiplication
            exp_result.operand1 = exp_calc.operand1 = None
            exp_result.operand2 = exp_calc.operand2 = self._number_factory.next()
        if exp_calc.operand1 is None:
            # ? / b = c -> b * c = ?
            exp_calc.operator = Operator.MUL
            return
        # a / ? = c -> a / c = ?
        exp_calc.operator = Operator.DIV
        _tmp = exp_calc.operand1
        exp_calc.operand1 = exp_calc.result
        exp_calc.result = _tmp

    def _resolve_mul(
        self,
        exp_calc: Expression,
        exp_result: Expression,
        operands_is_empty: bool,
        expression: Expression,
    ) -> bool:
        # a * b = c
        # a * ? = c -> c / a = b
        # ? * b = c -> c / b = a
        exp_calc.operator = Operator.DIV
        if not operands_is_empty:
            # one operand is missing -> will be calculated
            return True

        # one operand must be dividable by result
        try:
            exp_result.operand1 = exp_calc.operand1 = self._number_factory.next(
                dividable_by=exp_result.result,
                zero_allowed=False,
            )
            return True
        except ValueError as e:
            if expression.operator is None:
                return False
            raise ExpressionResolverNotResolvable(expression=expression, parent=e)

    def _calculate_result(self, exp_calc: Expression, exp_result: Expression) -> bool:
        if exp_result.operand1 is None:
            if is_zero_division(exp_calc.operator, exp_calc.operand2):
                return False
            exp_result.operand1 = self._calculate(
                exp_calc.result, exp_calc.operator, exp_calc.operand2
            )
            return True
        if exp_result.operand2 is None:
            if is_zero_division(exp_calc.operator, exp_calc.operand1):
                return False
            exp_result.operand2 = self._calculate(
                exp_calc.result, exp_calc.operator, exp_calc.operand1
            )
            return True
        raise RuntimeError("Invalid state: only one operand is missing")
