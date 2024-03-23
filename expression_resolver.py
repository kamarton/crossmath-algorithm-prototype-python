import random
import time

from expression import Expression, ExpressionValidator, Operator
from number_factory import NumberFactory


class ExpressionResolver:
    def __init__(self, validator: ExpressionValidator, number_factory: NumberFactory):
        self._validator = validator
        self._number_factory = number_factory
        pass

    def _fly_back(self, expression: Expression):
        self._number_factory.fly_back(expression.operand1)
        self._number_factory.fly_back(expression.operand2)
        self._number_factory.fly_back(expression.result)
        pass

    def _resolve_result_is_none(self, expression: Expression) -> Expression | None:
        while True:
            exp_result = expression.clone()
            if exp_result.operator is None:
                exp_result.operator = random.choice(Operator.get_operators_without_eq())
            if exp_result.operand1 is None:
                exp_result.operand1 = self._number_factory.next()
            if exp_result.operand2 is None:
                if exp_result.operator == Operator.SUB:
                    exp_result.operand2 = self._number_factory.next(
                        maximum=exp_result.operand1
                    )
                elif exp_result.operator == Operator.DIV and exp_result.operand1 != 0:
                    exp_result.operand2 = self._number_factory.next(
                        maximum=exp_result.operand1,
                        dividable_by=exp_result.operand1,
                        zero_allowed=False,
                    )
                else:
                    exp_result.operand2 = self._number_factory.next()
            exp_result.result = self._number_factory.fix(
                eval(
                    f"{exp_result.operand1} {exp_result.operator} {exp_result.operand2}"
                )
            )
            self._check_result(expression, exp_result)
            if not self._validator.validate(exp_result):
                # TODO time or count limit
                continue
            self._fly_back(exp_result)
            return exp_result

    def _resolve_result_is_available(self, expression: Expression) -> Expression | None:
        while True:
            exp_calc = expression.clone()
            exp_result = expression.clone()
            exp_result.result = expression.result
            operator = (
                expression.operator
                if expression.operator is not None
                else random.choice(Operator.get_operators_without_eq())
            )
            exp_result.operator = operator
            if exp_calc.operand1 is None and exp_calc.operand2 is None:
                exp_result.operand1 = exp_calc.operand1 = self._number_factory.next()
            if operator == Operator.ADD:
                # a + b = c
                # a + ? = c -> c - a = b
                # ? + b = c -> c - b = a
                exp_calc.operator = Operator.SUB
            elif operator == Operator.SUB:
                # a - b = c
                if exp_result.operand1 is None:
                    # ? - b = c -> c + b = a
                    exp_calc.operator = Operator.ADD
                else:
                    #  a - ? = c -> a - c = b
                    exp_calc.operator = Operator.SUB
                    _tmp = exp_calc.operand1
                    exp_calc.operand1 = exp_calc.result
                    exp_calc.result = _tmp
            elif operator == Operator.MUL:
                # a * b = c
                # a * ? = c -> c / a = b
                # ? * b = c -> c / b = a
                exp_calc.operator = Operator.DIV
            elif operator == Operator.DIV:
                # a / b = c
                if exp_calc.operand1 is None:
                    # ? / b = c -> b * c = ?
                    exp_calc.operator = Operator.MUL
                else:
                    # a / ? = c -> a / c = ?
                    exp_calc.operator = Operator.DIV
                    _tmp = exp_calc.operand1
                    exp_calc.operand1 = exp_calc.result
                    exp_calc.result = _tmp
            else:
                raise RuntimeError(f"Invalid operator: {operator}")
            if exp_result.operand1 is None:
                exp_result.operand1 = self._number_factory.fix(
                    eval(f"{exp_calc.result} {exp_calc.operator} {exp_calc.operand2}")
                )
            elif exp_result.operand2 is None:
                exp_result.operand2 = self._number_factory.fix(
                    eval(f"{exp_calc.result} {exp_calc.operator} {exp_calc.operand1}")
                )
            else:
                raise ValueError(f"Operator resolver not supported ({expression})")
            self._check_result(expression, exp_result)

            # print("expression:", expression, "exp_result:", exp_result)
            if not self._validator.validate(exp_result):
                # TODO time or count limit
                continue
            self._fly_back(exp_result)
            return exp_result

    def resolve(self, expression: Expression) -> Expression | None:
        start_time = time.time()
        try:
            if expression.result is None:
                return self._resolve_result_is_none(expression)
            return self._resolve_result_is_available(expression)
        finally:
            end_time = time.time()
            diff = end_time - start_time
            if diff > 0.01:
                print(f"ExpressionResolver.resolve: {diff:.2f} seconds")

    def _check_result(self, expression: Expression, result: Expression):
        if (
            (
                expression.operand1 is not None
                and not self._number_factory.is_equal(
                    expression.operand1, result.operand1
                )
            )
            or (
                expression.operand2 is not None
                and not self._number_factory.is_equal(
                    expression.operand2, result.operand2
                )
            )
            or (
                expression.result is not None
                and not self._number_factory.is_equal(expression.result, result.result)
            )
        ):
            raise RuntimeError(f"Invalid expression: {expression} -> {result}")
