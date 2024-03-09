import time

from expression import (
    ExpressionItems,
    ExpressionResolver,
    Expression,
    ExpressionItem,
    Direction,
)


class CrossMath:
    def __init__(self):
        self._items = ExpressionItems()
        self._expression_resolver = ExpressionResolver()

    def generate(self):
        start_time = time.time()

        for i in range(1):
            expression = Expression()
            expression = self._expression_resolver.resolve(expression)
            if expression is None:
                continue
            self._items.append(ExpressionItem(0, 0, Direction.HORIZONTAL, expression))
            print("time: ", time.time() - start_time)

    def print(self):
        self._items.print()
