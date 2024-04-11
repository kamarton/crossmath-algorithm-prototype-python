import random
import time

from expression import Expression, ExpressionValidator, Operator
from number_factory import NumberFactory


class ExpressionResolverException(Exception):
    def __init__(
        self,
        message: str = "Expression resolver exception",
        expression: Expression | None = None,
        parent: Exception | None = None,
    ):
        super().__init__(f"{message} (expression={expression}, parent={parent})")
        self._parent = parent


class ExpressionResolverNotResolvable(ExpressionResolverException):
    def __init__(
        self,
        message: str = "Expression is not resolvable",
        expression: Expression | None = None,
        parent: Exception | None = None,
    ):
        super().__init__(message, expression=expression, parent=parent)


class ExpressionResolverMaybeNotResolvable(ExpressionResolverException):
    def __init__(
        self,
        message: str = "Expression is maybe not resolvable",
        expression: Expression | None = None,
        parent: Exception | None = None,
    ):
        super().__init__(message, expression=expression, parent=parent)


class ExpressionResolver:
    def __init__(self, validator: ExpressionValidator, number_factory: NumberFactory):
        self._validator = validator
        self._number_factory = number_factory
        self._maximum_resolve_time_sec = 0.1

    def _fly_back(self, base: Expression, result: Expression):
        if base.operand1 is None:
            self._number_factory.fly_back(result.operand1)
        if base.operand2 is None:
            self._number_factory.fly_back(result.operand2)
        if base.result is None:
            self._number_factory.fly_back(result.result)

    def _fix_result(self, expression: Expression):
        expression.operand1 = self._number_factory.fix(expression.operand1)
        expression.operand2 = self._number_factory.fix(expression.operand2)
        expression.result = self._number_factory.fix(expression.result)

    def _next_operator(self, expression: Expression) -> list[Operator]:
        if expression.operand1 is None or expression.operand2 is None:
            yield random.choice(Operator.get_operators_without_eq())
        operators = Operator.get_operators_without_eq()
        random.shuffle(operators)
        for operator in operators:
            yield operator

    def _resolve_result_is_none(self, expression: Expression) -> Expression:
        start = time.time()
        operators = self._next_operator(expression)
        while time.time() - start < self._maximum_resolve_time_sec:
            exp_result = expression.clone()
            if exp_result.operator is None:
                try:
                    exp_result.operator = next(operators)
                except StopIteration:
                    raise ExpressionResolverNotResolvable(expression=expression)
            if exp_result.operator == Operator.DIV and NumberFactory.is_zero(
                exp_result.operand2
            ):
                continue
            if exp_result.operand1 is None:
                exp_result.operand1 = self._number_factory.next()
            if exp_result.operand2 is None:
                if exp_result.operator == Operator.SUB:
                    try:
                        exp_result.operand2 = self._number_factory.next(
                            maximum=exp_result.operand1
                        )
                    except ValueError as e:
                        raise ExpressionResolverNotResolvable(
                            expression=expression, parent=e
                        )
                elif exp_result.operator == Operator.DIV:
                    try:
                        exp_result.operand2 = self._number_factory.next(
                            maximum=exp_result.operand1,
                            dividable_by=exp_result.operand1,
                            zero_allowed=False,
                        )
                    except ValueError as e:
                        if expression.operator is None:
                            continue
                        raise ExpressionResolverNotResolvable(
                            expression=expression, parent=e
                        )
                else:
                    exp_result.operand2 = self._number_factory.next()
            exp_result.result = self._number_factory.fix(
                eval(
                    f"{exp_result.operand1} {exp_result.operator} {exp_result.operand2}"
                )
            )
            self._fix_result(exp_result)
            self._check_result(expression, exp_result)
            if not self._validator.validate(exp_result):
                # TODO time or count limit
                continue
            self._fly_back(expression, exp_result)
            return exp_result

        time_diff = time.time() - start
        raise ExpressionResolverMaybeNotResolvable(
            message=f"Too slow: {time_diff:.1f}s", expression=expression
        )

    def _resolve_only_operator_missing(self, expression: Expression) -> Expression:
        if (
            expression.operand1 is None
            or expression.operand2 is None
            or expression.result is None
            or expression.operator is not None
        ):
            raise RuntimeError(
                f"Invalid state, only operator missing is allowed: {expression}"
            )
        operators = Operator.get_operators_without_eq()
        random.shuffle(operators)
        for operator in operators:
            if operator == Operator.DIV and NumberFactory.is_zero(expression.operand2):
                # zero division
                continue
            exp_result = expression.clone()
            exp_result.operator = operator
            exp_result.result = self._number_factory.fix(
                eval(
                    f"{exp_result.operand1} {exp_result.operator} {exp_result.operand2}"
                )
            )
            if not NumberFactory.is_equal(exp_result.result, expression.result):
                continue
            self._fix_result(exp_result)
            self._check_result(expression, exp_result)
            if not self._validator.validate(exp_result):
                continue
            self._fly_back(expression, exp_result)
            return exp_result
        raise ExpressionResolverNotResolvable(expression=expression)

    def _resolve_result_is_available(self, expression: Expression) -> Expression:
        start = time.time()
        while time.time() - start < self._maximum_resolve_time_sec:
            exp_calc = expression.clone()
            exp_result = expression.clone()
            exp_result.result = expression.result
            operator = (
                expression.operator
                if expression.operator is not None
                else random.choice(Operator.get_operators_without_eq())
            )
            exp_result.operator = operator
            not_has_operands = exp_calc.operand1 is None and exp_calc.operand2 is None
            if not_has_operands:
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
                if not_has_operands:
                    try:
                        exp_result.operand1 = exp_calc.operand1 = (
                            self._number_factory.next(
                                dividable_by=exp_result.result,
                                zero_allowed=False,
                            )
                        )
                    except ValueError as e:
                        if expression.operator is None:
                            continue
                        raise ExpressionResolverNotResolvable(
                            expression=expression, parent=e
                        )
            elif operator == Operator.DIV:
                # a / b = c
                if not_has_operands:
                    exp_result.operand1 = exp_calc.operand1 = None
                    exp_result.operand2 = exp_calc.operand2 = (
                        self._number_factory.next()
                    )
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
                if ExpressionResolver.is_zero_division(
                    exp_calc.operator, exp_calc.operand2
                ):
                    continue
                exp_result.operand1 = self._number_factory.fix(
                    eval(f"{exp_calc.result} {exp_calc.operator} {exp_calc.operand2}")
                )
            elif exp_result.operand2 is None:
                if ExpressionResolver.is_zero_division(
                    exp_calc.operator, exp_calc.operand1
                ):
                    continue
                exp_result.operand2 = self._number_factory.fix(
                    eval(f"{exp_calc.result} {exp_calc.operator} {exp_calc.operand1}")
                )
            else:
                raise RuntimeError("Invalid state: only one operand is missing")
            self._check_result(expression, exp_result)

            if not self._validator.validate(exp_result):
                # TODO time or count limit
                continue
            self._fly_back(expression, exp_result)
            return exp_result

        time_diff = time.time() - start
        raise ExpressionResolverMaybeNotResolvable(
            message=f"Too slow: {time_diff:.1f}s", expression=expression
        )

    def resolve(self, expression: Expression) -> Expression | None:
        start_time = time.time()
        try:
            if expression.result is None:
                return self._resolve_result_is_none(expression)
            if expression.operand1 is not None and expression.operand2 is not None:
                return self._resolve_only_operator_missing(expression)
            return self._resolve_result_is_available(expression)
        finally:
            end_time = time.time()
            diff = end_time - start_time
            if diff > 0.01:
                print(f"ExpressionResolver.resolve: {diff:.2f} seconds")

    def _check_result(self, expression: Expression, result: Expression):
        if expression.operand1 is not None:
            if not NumberFactory.is_equal(expression.operand1, result.operand1):
                raise RuntimeError(f"Invalid operand1: {expression} -> {result}")
        if expression.operand2 is not None:
            if not NumberFactory.is_equal(expression.operand2, result.operand2):
                raise RuntimeError(f"Invalid operand2: {expression} -> {result}")
        if expression.result is not None:
            if not NumberFactory.is_equal(expression.result, result.result):
                raise RuntimeError(f"Invalid result: {expression} -> {result}")
        if expression.operator is not None:
            if expression.operator != result.operator:
                raise RuntimeError(f"Invalid operator: {expression} -> {result}")

    @staticmethod
    def is_zero_division(operator: Operator, operand2: float) -> bool:
        return operator == Operator.DIV and NumberFactory.is_zero(operand2)
