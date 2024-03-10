import random
import time
from typing import Tuple

from expression import (
    ExpressionItems,
    Expression,
    ExpressionItem,
    Direction,
)
from expression_resolver import ExpressionResolver


class CrossMath:
    def __init__(self):
        self._items = ExpressionItems()
        self._expression_resolver = ExpressionResolver()

    def _find_potential_positions(self, items_map: list[list]) -> list[Tuple[int, int]]:
        for y in range(len(items_map)):
            for x in range(len(items_map[y])):
                value = items_map[y][x]
                if isinstance(value, int):
                    yield x, y

    def _find_potential_values(
        self, potential_positions: list[Tuple[int, int]]
    ) -> list[Tuple[Direction, int, int, list]]:
        for next_position in potential_positions:
            x, y = next_position
            slice_offset = -1
            slice_length = ExpressionItem.LENGTH - slice_offset
            values_offset = -slice_offset
            for direction in [Direction.HORIZONTAL, Direction.VERTICAL]:
                x_offset = 0 if direction == Direction.VERTICAL else slice_offset
                y_offset = 0 if direction == Direction.HORIZONTAL else slice_offset
                values = self._items.get_values(
                    x + x_offset, y + y_offset, direction, slice_length
                )
                if values[0] is None and values[2] is None:
                    yield (
                        direction,
                        x,
                        y,
                        values[values_offset:],
                    )

    def _init_generate(self):
        expression = self._expression_resolver.resolve(Expression())
        if expression is None:
            raise Exception("No expression found")
        direction = random.choice([Direction.HORIZONTAL, Direction.VERTICAL])
        self._items.append(ExpressionItem(0, 0, direction, expression))

    def generate(self):
        start_time = time.time()
        self._init_generate()
        for i in range(20):
            items_map = self._items.get_map()
            potential_positions = self._find_potential_positions(items_map)
            potential_values = list(self._find_potential_values(potential_positions))
            random.shuffle(potential_values)
            is_expression_appended = False
            for desc in potential_values:
                direction, _x, _y, values = desc
                # print("desc:", desc, "x:", _x, "y:", _y)
                try:
                    expression = self._expression_resolver.resolve(
                        Expression.instance_from_values(values)
                    )
                except ValueError:
                    # TODO store dead positions
                    continue
                if expression is None:
                    # TODO store dead positions
                    continue
                expression_item = ExpressionItem(_x, _y, direction, expression)
                self._items.append(expression_item)
                is_expression_appended = True
                break
            if not is_expression_appended:
                break

            print("time: ", time.time() - start_time)

    def print(self):
        self._items.print()
