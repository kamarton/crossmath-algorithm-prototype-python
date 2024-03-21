import random
import time

from expression import Expression, ExpressionValidator, Operator


class OperandFactory:

    def __init__(self):
        self._number_stat: dict[int, int] = {}

    def next(self):
        return random.randint(1, 10)

    def fly_back(self, value: int):
        if value not in self._number_stat:
            self._number_stat[value] = 0
        self._number_stat[value] += 1


class ExpressionResolver:
    def __init__(self):
        self._expression_validator = ExpressionValidator()
        self._operand_factory = OperandFactory()
        pass

    def _fly_back(self, expression: Expression):
        self._operand_factory.fly_back(expression.operand1)
        self._operand_factory.fly_back(expression.operand2)
        self._operand_factory.fly_back(expression.result)
        pass

    def resolve(self, expression: Expression) -> Expression | None:
        start_time = time.time()
        try:
            if expression.result is None:
                while True:
                    exp_result = expression.clone()
                    if exp_result.operand1 is None:
                        exp_result.operand1 = self._operand_factory.next()
                    if exp_result.operand2 is None:
                        exp_result.operand2 = self._operand_factory.next()
                    if exp_result.operator is None:
                        exp_result.operator = random.choice(
                            Operator.get_operators_without_eq()
                        )
                    exp_result.result = eval(
                        f"{exp_result.operand1} {exp_result.operator} {exp_result.operand2}"
                    )
                    exp_result.result = int(exp_result.result)
                    if not self._expression_validator.validate(exp_result):
                        if time.time() - start_time > 0.5:
                            print(f"ExpressionResolver.resolve: timeout ({expression})")
                            return None
                        continue
                    self._fly_back(exp_result)
                    return exp_result
            else:  # result is available
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
                        exp_result.operand1 = exp_calc.operand1 = (
                            self._operand_factory.next()
                        )
                    if operator == Operator.ADD:
                        # a + b = c   a + ? = c -> c - a = b   ? + b = c -> c - b = a
                        exp_calc.operator = Operator.SUB
                    elif operator == Operator.SUB:
                        # a - b = c   a - ? = c -> a - c = b   ? - b = c -> c + b = a
                        if exp_result.operand1 is None:
                            exp_calc.operator = Operator.ADD
                        else:
                            exp_calc.operator = Operator.SUB
                            _tmp = exp_calc.operand1
                            exp_calc.operand1 = exp_calc.result
                            exp_calc.result = _tmp
                    elif operator == Operator.MUL:
                        # a * b = c   a * ? = c -> c / a = b   ? * b = c -> c / b = a
                        exp_calc.operator = Operator.DIV
                    elif operator == Operator.DIV:
                        # a / b = c   a / ? = c -> a / c = ?   ? / b = c -> b * c = ?
                        if exp_calc.operand1 is None:
                            exp_calc.operator = Operator.MUL
                        else:
                            exp_calc.operator = Operator.DIV
                            _tmp = exp_calc.operand1
                            exp_calc.operand1 = exp_calc.result
                            exp_calc.result = _tmp
                    else:
                        raise RuntimeError(f"Invalid operator: {operator}")
                    if exp_result.operand1 is None:
                        exp_result.operand1 = int(
                            eval(
                                f"{exp_calc.result} {exp_calc.operator} {exp_calc.operand2}"
                            )
                        )
                    elif exp_result.operand2 is None:
                        exp_result.operand2 = int(
                            eval(
                                f"{exp_calc.result} {exp_calc.operator} {exp_calc.operand1}"
                            )
                        )
                    else:
                        raise ValueError(
                            f"Operator resolver not supported ({expression})"
                        )

                    # print("expression:", expression, "exp_result:", exp_result)
                    if (
                        (
                            expression.operand1 is not None
                            and expression.operand1 != exp_result.operand1
                        )
                        or (
                            expression.operand2 is not None
                            and expression.operand2 != exp_result.operand2
                        )
                        or (expression.result != exp_result.result)
                    ):
                        raise RuntimeError(
                            f"Invalid expression: {expression} -> {exp_result}"
                        )
                    if not self._expression_validator.validate(exp_result):
                        if time.time() - start_time > 0.2:
                            print(f"ExpressionResolver.resolve: timeout ({expression})")
                            return None
                        continue
                    self._fly_back(exp_result)
                    return exp_result
            return None
        finally:
            end_time = time.time()
            diff = end_time - start_time
            if diff > 0.01:
                print(f"ExpressionResolver.resolve: {diff:.2f} seconds")
