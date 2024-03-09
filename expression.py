import random
from enum import Enum

import pandas


class Operator(Enum):
    ADD = "+"
    SUB = "-"
    # MUL = '*'
    # DIV = '/'
    EQ = "="

    @staticmethod
    def get_operators_without_eq() -> list:
        # return [Operators.ADD, Operators.SUB, Operators.MUL, Operators.DIV]
        return [Operator.ADD, Operator.SUB]

    def __str__(self):
        return self.value


class Direction(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

    def __str__(self):
        return self.name


class Expression:
    def __init__(self):
        self.operator: Operator | None = None
        self.operand1: int | None = None
        self.operand2: int | None = None
        self.result: int | None = None

    def get_values(self) -> list:
        return [self.operand1, self.operator, self.operand2, Operator.EQ, self.result]

    def is_empty(self) -> bool:
        return (
            self.operator is None
            and self.operand1 is None
            and self.operand2 is None
            and self.result is None
        )

    def __str__(self):
        return f"{self.operand1} {self.operator} {self.operand2} = {self.result}"


class ExpressionValidator:
    def __int__(self):
        pass

    def validate(self, expression: Expression) -> bool:
        if (
            expression.operator is None
            or expression.operand1 is None
            or expression.operand2 is None
            or expression.result is None
        ):
            return False
        if expression.operand1 < 0:
            return False
        if expression.operand2 < 0:
            return False
        if expression.result < 0:
            return False
        return True


class ExpressionItem:
    def __init__(self, x: int, y: int, direction: Direction, expression: Expression):
        self._x = x
        self._y = y
        self._direction = direction
        self._expression = expression

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def get_direction(self) -> Direction:
        return self._direction

    def get_expression(self) -> Expression:
        return self._expression

    def get_length(self) -> int:
        return 5

    def get_width(self) -> int:
        return self.get_length() if self.get_direction() == Direction.HORIZONTAL else 1

    def get_height(self) -> int:
        return 1 if self.get_direction() == Direction.HORIZONTAL else self.get_length()

    def __str__(self):
        return f"x: {self.get_x()}, y: {self.get_y()}, direction: {self.get_direction()}, expression: {self.get_expression()}"


class ExpressionItems(list):
    def __init__(self):
        super().__init__()

    def get_min_x(self) -> int:
        return min([item.get_x() for item in self])

    def get_max_x(self) -> int:
        return max([item.get_x() + item.get_width() for item in self])

    def get_min_y(self) -> int:
        return min([item.get_y() for item in self])

    def get_max_y(self) -> int:
        return max([item.get_y() + item.get_height() for item in self])

    def print(self):
        rows = [
            [None for _ in range(self.get_min_x(), self.get_max_x())]
            for _ in range(self.get_min_y(), self.get_max_y())
        ]
        for item in self:
            values = item.get_expression().get_values()
            x = item.get_x()
            y = item.get_y()
            x_add = 1 if item.get_direction() == Direction.HORIZONTAL else 0
            y_add = 1 if item.get_direction() == Direction.VERTICAL else 0
            for value in values:
                rows[y][x] = value
                x += x_add
                y += y_add

        df = pandas.DataFrame(rows)
        print(df)


class ExpressionResolver:
    def __init__(self):
        self._expression_validator = ExpressionValidator()
        pass

    def resolve(self, expression: Expression) -> Expression | None:
        if expression.is_empty():
            while True:
                expression.operand1 = random.randint(1, 9)
                expression.operand2 = random.randint(1, 9)
                expression.operator = random.choice(Operator.get_operators_without_eq())
                expression.result = eval(
                    f"{expression.operand1} {expression.operator} {expression.operand2}"
                )
                if not self._expression_validator.validate(expression):
                    continue
                return expression
        return None
