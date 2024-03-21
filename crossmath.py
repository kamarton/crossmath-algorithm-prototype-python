import random
import time
from typing import Tuple

from expression import Expression
from expression_map import ExpressionMap, ExpressionItem, Direction
from expression_resolver import ExpressionResolver


class CrossMath:
    def __init__(self, exp_map: ExpressionMap):
        self._map = exp_map
        self._expression_resolver = ExpressionResolver()

    def _find_potential_positions(self) -> list[Tuple[int, int]]:
        for y in range(self._map.height()):
            for x in range(self._map.width()):
                value = self._map.get(x, y)
                if isinstance(value, int):
                    yield x, y

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
        self, potential_positions: list[Tuple[int, int]]
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
            3,
            3,
            direction,
            expression,
        )
        self._map.put(item)

    def generate(self):
        start_time = time.time()
        self._init_generate()
        for i in range(40):
            potential_positions = self._find_potential_positions()
            potential_values = list(self._find_potential_values(potential_positions))
            random.shuffle(potential_values)
            is_expression_appended = False
            for desc in potential_values:
                direction, _x, _y, values = desc
                # print("desc:", desc, "x:", _x, "y:", _y)
                try:
                    expression = self._expression_resolver.resolve(
                        Expression.from_values(values)
                    )
                except ValueError:
                    # TODO store dead positions
                    continue
                if expression is None:
                    # TODO store dead positions
                    continue
                expression_item = ExpressionItem(_x, _y, direction, expression)
                self._map.put(expression_item)
                is_expression_appended = True
                break
            if not is_expression_appended:
                break

            print("time: ", time.time() - start_time)

    def print(self):
        self._map.print()
