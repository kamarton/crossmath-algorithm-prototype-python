import random
import time
from typing import Tuple

from expression import (
    ExpressionItems,
    Expression,
    ExpressionItem,
    Direction,
    Operator,
)
from expression_resolver import ExpressionResolver


class CrossMath:
    def __init__(self):
        self._items = ExpressionItems()
        self._expression_resolver = ExpressionResolver()

    def _find_next_positions(self, items_map: list[list]) -> list[Tuple[int, int]]:
        result = []
        for y in range(len(items_map)):
            for x in range(len(items_map[y])):
                value = items_map[y][x]
                # if value in Operator.get_operators_without_eq():
                #     result.append((x, y))
                if isinstance(value, int):
                    result.append((x, y))
        return result

    def _init_generate(self):
        expression = self._expression_resolver.resolve(Expression())
        if expression is None:
            raise Exception("No expression found")
        direction = random.choice([Direction.HORIZONTAL, Direction.VERTICAL])
        self._items.append(ExpressionItem(0, 0, direction, expression))

    def generate(self):
        start_time = time.time()
        self._init_generate()
        for i in range(30):
            items_map = self._items.get_map()
            next_positions = self._find_next_positions(items_map)
            if len(next_positions) == 0:
                break
            random.shuffle(next_positions)
            # print("next_positions: ", next_positions)
            for next_position in next_positions:
                x, y = next_position
                slice_offset = -1
                slice_length = ExpressionItem.LENGTH + 1
                values_offset = 1
                values_horizontally = self._items.get_values(
                    x + slice_offset, y, Direction.HORIZONTAL, slice_length
                )
                values_vertically = self._items.get_values(
                    x, y + slice_offset, Direction.VERTICAL, slice_length
                )

                values_for_expression = []
                if values_horizontally[0] is None and values_horizontally[2] is None:
                    values_for_expression.append(
                        [
                            Direction.HORIZONTAL,
                            x + slice_offset + values_offset,
                            y,
                            values_horizontally[values_offset:],
                        ]
                    )
                if values_vertically[0] is None and values_vertically[2] is None:
                    values_for_expression.append(
                        [
                            Direction.VERTICAL,
                            x,
                            y + slice_offset + values_offset,
                            values_vertically[values_offset:],
                        ]
                    )
                if len(values_for_expression) == 0:
                    # TODO store dead positions
                    continue

                random.shuffle(values_for_expression)
                is_expression_appended = False
                for desc in values_for_expression:
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
                if is_expression_appended:
                    break

            print("time: ", time.time() - start_time)

    def print(self):
        self._items.print()
