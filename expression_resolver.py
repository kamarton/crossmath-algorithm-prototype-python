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
            if expression.is_empty():
                while True:
                    expression.operand1 = self._operand_factory.next()
                    expression.operand2 = self._operand_factory.next()
                    expression.operator = random.choice(
                        Operator.get_operators_without_eq()
                    )
                    expression.result = eval(
                        f"{expression.operand1} {expression.operator} {expression.operand2}"
                    )
                    if not self._expression_validator.validate(expression):
                        continue
                    expression.result = int(expression.result)
                    self._fly_back(expression)
                    return expression
            if expression.operator is not None and expression.result is None:
                while True:
                    exp_clone = expression.clone()
                    if exp_clone.operand1 is None:
                        exp_clone.operand1 = self._operand_factory.next()
                    if exp_clone.operand2 is None:
                        exp_clone.operand2 = self._operand_factory.next()
                    exp_clone.result = eval(
                        f"{exp_clone.operand1} {exp_clone.operator} {exp_clone.operand2}"
                    )
                    if not self._expression_validator.validate(exp_clone):
                        continue
                    exp_clone.result = int(exp_clone.result)
                    self._fly_back(exp_clone)
                    return exp_clone
            if expression.operand1 is not None and expression.result is None:
                while True:
                    exp_clone = expression.clone()
                    if exp_clone.operator is None:
                        exp_clone.operator = random.choice(
                            Operator.get_operators_without_eq()
                        )
                    if exp_clone.operand2 is None:
                        exp_clone.operand2 = self._operand_factory.next()
                    exp_clone.result = eval(
                        f"{exp_clone.operand1} {exp_clone.operator} {exp_clone.operand2}"
                    )
                    if not self._expression_validator.validate(exp_clone):
                        continue
                    exp_clone.result = int(exp_clone.result)
                    self._fly_back(exp_clone)
                    return exp_clone
            return None
        finally:
            end_time = time.time()
            diff = end_time - start_time
            if diff > 0.01:
                print(f"ExpressionResolver.resolve: {diff:.2f} seconds")
