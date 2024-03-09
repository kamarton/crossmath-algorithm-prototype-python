import random
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

    def _init_generate(self):
        expression = self._expression_resolver.resolve(Expression())
        if expression is None:
            raise Exception("No expression found")
        direction = random.choice([Direction.HORIZONTAL, Direction.VERTICAL])
        self._items.append(ExpressionItem(0, 0, direction, expression))

    def generate(self):
        start_time = time.time()
        self._init_generate()
        for i in range(1):
            print("time: ", time.time() - start_time)

    def print(self):
        self._items.print()
