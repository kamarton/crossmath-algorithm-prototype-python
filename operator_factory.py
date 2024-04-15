import random
from enum import Enum


class Operator(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    EQ = "="

    @staticmethod
    def get_operators_without_eq() -> list:
        """
        Returns a list of operators without the equal operator.
        """
        return [Operator.ADD, Operator.SUB, Operator.MUL, Operator.DIV]

    def __str__(self):
        return self.value


class OperatorFactory:
    def __init__(self, operators: list[Operator] | None = None):
        self._operators = (
            operators if operators is not None else Operator.get_operators_without_eq()
        )
        self._stats = {operator: 0 for operator in self._operators}

    def next_weighted_operator(
        self, excludes: list[Operator] | None = None
    ) -> Operator:
        operators = self.operators_weighted(excludes=excludes)
        return random.choice(operators)

    def operators_weighted(
        self, excludes: list[Operator] | None = None
    ) -> list[Operator]:
        if excludes is None:
            excludes = []
        # TODO smarter weighting
        operators = sorted(self._operators, key=lambda operator: self._stats[operator])
        for operator in excludes:
            operators.remove(operator)
        return operators

    def iter_weighted_operators(self, excludes: list) -> Operator:
        # TODO smarter weighting
        for operator in self.operators_weighted(excludes):
            yield operator
        for operator in self._operators:
            if operator not in excludes:
                yield operator

    def operators(self) -> list[Operator]:
        return self._operators

    def fly_back(self, operator: Operator):
        self._stats[operator] += 1

    def print_statistic(self):
        for operator, count in self._stats.items():
            print(f"{operator}: {count}")
