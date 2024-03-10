from enum import Enum
from typing import TypeVar

import pandas

Exp = TypeVar("Exp", bound="Expression")


class Operator(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    EQ = "="

    @staticmethod
    def get_operators_without_eq() -> list:
        return [Operator.ADD, Operator.SUB, Operator.MUL, Operator.DIV]

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

    @staticmethod
    def instance_from_values(values: list) -> Exp:
        expression = Expression()
        expression.operand1 = values[0]
        expression.operator = values[1]
        expression.operand2 = values[2]
        if values[3] is not None and values[3] != Operator.EQ:
            raise ValueError("Invalid values (EQ)")
        expression.result = values[4]
        return expression

    def clone(self) -> Exp:
        expression = Expression()
        expression.operand1 = self.operand1
        expression.operator = self.operator
        expression.operand2 = self.operand2
        expression.result = self.result
        return expression

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
        if expression.operand1 < 1 or expression.operand1 > 100:
            return False
        if expression.operand2 < 1 or expression.operand2 > 100:
            return False
        if expression.result < 1 or expression.result > 100:
            return False
        return True


class ExpressionItem:

    LENGTH = 5

    def __init__(self, x: int, y: int, direction: Direction, expression: Expression):
        self._x = x
        self._y = y
        self._direction = direction
        self._expression = expression

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def add_x(self, x_add: int):
        self._x += x_add

    def add_y(self, y_add: int):
        self._y += y_add

    def get_direction(self) -> Direction:
        return self._direction

    def get_expression(self) -> Expression:
        return self._expression

    def get_length(self) -> int:
        return self.LENGTH

    def get_width(self) -> int:
        return self.get_length() if self.get_direction() == Direction.HORIZONTAL else 1

    def get_height(self) -> int:
        return 1 if self.get_direction() == Direction.HORIZONTAL else self.get_length()

    def __str__(self):
        return f"x: {self.get_x()}, y: {self.get_y()}, direction: {self.get_direction()}, expression: {self.get_expression()}"


class ExpressionItems(list):
    def __init__(self):
        super().__init__()
        self._map: list[list[ExpressionItem]] = list()
        self._min_x: int | None = 0
        self._max_x: int | None = 0
        self._min_y: int | None = 0
        self._max_y: int | None = 0

    def get_min_x(self) -> int:
        return self._min_x

    def get_max_x(self) -> int:
        return self._max_x

    def get_min_y(self) -> int:
        return self._min_y

    def get_max_y(self) -> int:
        return self._max_y

    def append(self, __object, fix_positions: bool = True):
        if fix_positions:
            __object.add_x(self.get_min_x())
            __object.add_y(self.get_min_y())
        super().append(__object)
        self._refresh_map()

    def _refresh_map(self):
        self._min_x = self._min_y = self._max_x = self._max_y = 0
        for item in self:
            self._min_x = min(self._min_x, item.get_x())
            self._min_y = min(self._min_y, item.get_y())
            self._max_x = max(self._max_x, item.get_x() + item.get_width())
            self._max_y = max(self._max_y, item.get_y() + item.get_height())
        self._map = [
            [None for _ in range(self.get_min_x(), self.get_max_x())]
            for _ in range(self.get_min_y(), self.get_max_y())
        ]
        for item in self:
            values = item.get_expression().get_values()
            x = item.get_x() - self.get_min_x()
            y = item.get_y() - self.get_min_y()
            x_add = 1 if item.get_direction() == Direction.HORIZONTAL else 0
            y_add = 1 if item.get_direction() == Direction.VERTICAL else 0
            for value in values:
                self._map[y][x] = value
                x += x_add
                y += y_add

    def get_map(self) -> list[list]:
        return self._map

    def get_values(self, x: int, y: int, direction: Direction, length: int) -> list:
        result = []
        x_add = 1 if direction == Direction.HORIZONTAL else 0
        y_add = 1 if direction == Direction.VERTICAL else 0
        min_x = self.get_min_x()
        min_y = self.get_min_y()
        max_x = self.get_max_x()
        max_y = self.get_max_y()
        x -= min_x
        y -= min_y
        for _ in range(length):
            if x < 0 or x >= max_x - min_x or y < 0 or y >= max_y - min_y:
                result.append(None)
            else:
                result.append(self._map[y][x])
            x += x_add
            y += y_add
        return result

    def print(self):
        map_clone = []
        for row in self._map:
            map_clone.append(["" if x is None else str(x) for x in row])
        pandas.set_option("display.max_rows", None)
        pandas.set_option("display.max_columns", None)
        pandas.set_option("display.width", 2000)
        df = pandas.DataFrame(map_clone)
        print(df)
        pandas.reset_option("display.max_rows")
        pandas.reset_option("display.max_columns")
        pandas.reset_option("display.width")
