import random
import time
from typing import Tuple

from expression import Expression, ExpressionValidator
from expression_map import (
    ExpressionMap,
    ExpressionItem,
    Direction,
    ExpressionMapCellValueMissmatch,
)
from expression_resolver import (
    ExpressionResolver,
    ExpressionResolverException,
)
from number_factory import NumberFactory


class DeadPoints:
    def __init__(self):
        self._data: dict[Tuple[int, int], list[Direction]] = {}

    def add(self, x: int, y: int, direction: Direction):
        if (x, y) not in self._data:
            self._data[(x, y)] = []
        self._data[(x, y)].append(direction)

    def is_dead(self, x: int, y: int, direction: Direction) -> bool:
        if (x, y) not in self._data:
            return False
        return direction in self._data[(x, y)]

    def is_dead_full(self, x: int, y: int) -> bool:
        if (x, y) not in self._data:
            return False
        return len(self._data[(x, y)]) == len(Direction.all())

    def clear(self):
        self._data.clear()


class CrossMath:
    def __init__(
        self,
        exp_map: ExpressionMap,
        number_factory: NumberFactory,
        expression_resolver: ExpressionResolver,
    ):
        self._map = exp_map
        self._number_factory = number_factory
        self._expression_resolver = expression_resolver
        self._dead_points = DeadPoints()

    def _find_potential_positions(self) -> list[Tuple[int, int]]:
        for point in self._map.get_all_operand_points():
            x, y = point
            if self._dead_points.is_dead_full(x, y):
                continue
            yield point

    def _check_expression_frame(
        self, x: int, y: int, direction: Direction, length: int
    ) -> bool:
        if direction.is_horizontal():
            if x > 0 and self._map.get(x - 1, y) is not None:
                return False
            if (
                x + length + 1 < self._map.width()
                and self._map.get(x + length + 1, y) is not None
            ):
                return False
        elif direction.is_vertical():
            if y > 0 and self._map.get(x, y - 1) is not None:
                return False
            if (
                y + length + 1 < self._map.height()
                and self._map.get(x, y + length + 1) is not None
            ):
                return False
        else:
            raise ValueError(f"Not supported direction: {direction}")
        return True

    def _check_x_y_overflow(self, x: int, y: int, length: int) -> bool:
        if x < 0:
            return False
        elif x + length >= self._map.width():
            return False
        elif y < 0:
            return False
        elif y + length >= self._map.height():
            return False
        return True

    def _find_potential_values(
        self,
        potential_positions: list[Tuple[int, int]],
    ) -> list[Tuple[Direction, int, int, list]]:
        max_expression_length = max(Expression.SUPPORTED_LENGTHS)
        for next_position in potential_positions:
            x, y = next_position
            for direction in Direction.all():
                for expression_offset in range(0, -max_expression_length - 1, -2):
                    values_x_offset = (
                        0 if direction.is_vertical() else expression_offset
                    )
                    values_y_offset = (
                        0 if direction.is_horizontal() else expression_offset
                    )
                    for expression_length in Expression.SUPPORTED_LENGTHS:
                        values_x = x + values_x_offset
                        values_y = y + values_y_offset
                        if not self._check_x_y_overflow(
                            values_x, values_y, expression_length
                        ):
                            continue

                        if not self._check_expression_frame(
                            values_x, values_y, direction, expression_length
                        ):
                            continue

                        values = self._map.get_values(
                            values_x, values_y, direction, expression_length
                        )
                        if all([value is not None for value in values]):
                            # already filled
                            continue
                        if self._dead_points.is_dead(values_x, values_y, direction):
                            continue

                        yield (
                            direction,
                            values_x,
                            values_y,
                            values,
                        )

    def _init_generate(self):
        expression = self._expression_resolver.resolve(Expression())
        if expression is None:
            raise Exception("No expression found")
        direction = random.choice([Direction.HORIZONTAL, Direction.VERTICAL])
        item = ExpressionItem(
            2,
            2,
            direction,
            expression,
        )
        self._map.put(item)

    def generate(self):
        self._dead_points.clear()
        self._init_generate()
        latest_version = None
        while latest_version != self._map.get_version():
            latest_version = self._map.get_version()
            potential_values = self._find_potential_values(
                potential_positions=self._find_potential_positions(),
            )
            pvs = list(potential_values)
            random.shuffle(pvs)
            for desc in pvs:
                direction, _x, _y, values = desc
                try:
                    expression = self._expression_resolver.resolve(
                        Expression.from_list(values)
                    )
                except ExpressionResolverException as e:
                    print(e)
                    self._dead_points.add(_x, _y, direction)
                    continue
                expression_item = ExpressionItem(_x, _y, direction, expression)
                self._map.put(expression_item)
                break

    def print(self):
        self._map.print(number_factory=self._number_factory)
