import random
import time

from expression import Expression, ExpressionValidator, Operator


class ExpressionResolver:
    def __init__(self):
        self._expression_validator = ExpressionValidator()
        pass

    def resolve(self, expression: Expression) -> Expression | None:
        start_time = time.time()
        try:
            if expression.is_empty():
                while True:
                    expression.operand1 = random.randint(1, 9)
                    expression.operand2 = random.randint(1, 9)
                    expression.operator = random.choice(
                        Operator.get_operators_without_eq()
                    )
                    expression.result = eval(
                        f"{expression.operand1} {expression.operator} {expression.operand2}"
                    )
                    if not self._expression_validator.validate(expression):
                        continue
                    expression.result = int(expression.result)
                    return expression
            if expression.operator is not None and expression.result is None:
                while True:
                    exp_clone = expression.clone()
                    if exp_clone.operand1 is None:
                        exp_clone.operand1 = random.randint(1, 9)
                    if exp_clone.operand2 is None:
                        exp_clone.operand2 = random.randint(1, 9)
                    exp_clone.result = eval(
                        f"{exp_clone.operand1} {exp_clone.operator} {exp_clone.operand2}"
                    )
                    if not self._expression_validator.validate(exp_clone):
                        continue
                    exp_clone.result = int(exp_clone.result)
                    return exp_clone
            if expression.operand1 is not None and expression.result is None:
                while True:
                    exp_clone = expression.clone()
                    if exp_clone.operator is None:
                        exp_clone.operator = random.choice(
                            Operator.get_operators_without_eq()
                        )
                    if exp_clone.operand2 is None:
                        exp_clone.operand2 = random.randint(1, 9)
                    exp_clone.result = eval(
                        f"{exp_clone.operand1} {exp_clone.operator} {exp_clone.operand2}"
                    )
                    if not self._expression_validator.validate(exp_clone):
                        continue
                    exp_clone.result = int(exp_clone.result)
                    return exp_clone
            return None
        finally:
            end_time = time.time()
            diff = end_time - start_time
            if diff > 0.01:
                print(f"ExpressionResolver.resolve: {diff:.2f} seconds")
