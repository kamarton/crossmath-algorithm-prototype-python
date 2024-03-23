from enum import Enum

import pandas

from expression import Expression, Operator
from number_factory import NumberFactory


class Direction(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

    @staticmethod
    def all() -> list:
        return [Direction.HORIZONTAL, Direction.VERTICAL]

    def is_horizontal(self) -> bool:
        return self == Direction.HORIZONTAL

    def is_vertical(self) -> bool:
        return self == Direction.VERTICAL

    def __str__(self):
        return self.name


class ExpressionItem:
    def __init__(self, x: int, y: int, direction: Direction, expression: Expression):
        self._x = x
        self._y = y
        self._direction = direction
        self._expression = expression

    def x(self) -> int:
        return self._x

    def y(self) -> int:
        return self._y

    def is_horizontal(self) -> bool:
        return self._direction == Direction.HORIZONTAL

    def is_vertical(self) -> bool:
        return self._direction == Direction.VERTICAL

    def direction(self) -> Direction:
        return self._direction

    def expression(self) -> Expression:
        return self._expression

    def length(self) -> int:
        return self._expression.get_length()

    def width(self) -> int:
        return self.length() if self.direction() == Direction.HORIZONTAL else 1

    def height(self) -> int:
        return 1 if self.direction() == Direction.HORIZONTAL else self.length()

    def __str__(self):
        return f"x: {self.x()}, y: {self.y()}, direction: {self.direction()}, length: {self.length()}, expression: {self.expression()}"


class ExpressionMap:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._map: list[list[Operator | None | float]] = [
            [None for _ in range(width)] for _ in range(height)
        ]

    def width(self) -> int:
        return self._width

    def height(self) -> int:
        return self._height

    def get(self, x: int, y: int) -> Operator | None | float:
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            raise ValueError(f"Invalid x, y: {x}, {y}")
        return self._map[y][x]

    def get_values(self, x: int, y: int, direction: Direction, length: int):
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            raise ValueError(f"Invalid x, y: {x}, {y}")
        if direction == Direction.HORIZONTAL:
            if x + length > self._width:
                raise ValueError(f"Invalid x, length: {x}, {length}")
            return self._map[y][x : x + length]
        if y + length > self._height:
            raise ValueError(f"Invalid y, length: {y}, {length}")
        return [self._map[y + i][x] for i in range(length)]

    def put(self, item: ExpressionItem):
        x = item.x()
        y = item.y()
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            raise ValueError(f"Invalid x, y: {x}, {y}")
        values = item.expression().values()
        if item.is_horizontal():
            if x + len(values) > self._width:
                raise ValueError(f"Invalid x, length: {x}, {len(values)}")
        elif item.is_vertical():
            if y + len(values) > self._height:
                raise ValueError(f"Invalid y, length: {y}, {len(values)}")
        else:
            raise ValueError(f"Not supported direction: {item.direction()}")
        # pre checking values and destination
        for i in range(len(values)):
            if item.is_horizontal():
                if self._map[y][x + i] is not None and self._map[y][x + i] != values[i]:
                    raise ValueError(
                        f"Illegal override x, y, values: {x}, {y}, {self._map[y][x + i]}, {values[i]}"
                    )
            else:
                if self._map[y + i][x] is not None and self._map[y + i][x] != values[i]:
                    raise ValueError(
                        f"Illegal override x, y, values: {x}, {y}, {self._map[y + i][x]}, {values[i]}"
                    )
        for i in range(len(values)):
            if item.is_horizontal():
                self._map[y][x + i] = values[i]
            else:
                self._map[y + i][x] = values[i]

    def print(self, number_factory: NumberFactory | None = None):
        pandas.set_option("display.max_rows", None)
        pandas.set_option("display.max_columns", None)
        pandas.set_option("display.width", 2000)
        map_clear = [["" for _ in range(self._width)] for _ in range(self._height)]
        for y in range(self._height):
            for x in range(self._width):
                if self._map[y][x] is not None:
                    map_clear[y][x] = self._map[y][x]
                    is_numeric = isinstance(self._map[y][x], float)
                    if number_factory is not None and is_numeric:
                        map_clear[y][x] = number_factory.format(self._map[y][x])
        df = pandas.DataFrame(map_clear)
        print(df)
        pandas.reset_option("display.max_rows")
        pandas.reset_option("display.max_columns")
        pandas.reset_option("display.width")
