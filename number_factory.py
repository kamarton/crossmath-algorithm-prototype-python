import math
import random


class NumberFactory:

    def __init__(self, minimum: float = 1.0, maximum: float = 10.0, step: float = 1):
        self._number_stat: dict[str, int] = {}
        self._min: float = minimum
        self._max: float = maximum
        if step <= 0:
            raise ValueError("Step must be greater than 0")
        self._step = step
        self._decimals: int = max(0, -1 * math.floor(math.log10(step)))

    def next(
        self,
        minimum: float | None = None,
        maximum: float | None = None,
        dividable_by: float | None = None,
        zero_allowed: bool = True,
    ) -> float:
        # TODO add support for negative numbers
        if dividable_by is not None:
            if self.is_equal(dividable_by, 0.0):
                dividable_by = None
            else:
                dividable_by = abs(dividable_by)
        full_range = abs((maximum or self._max) - (minimum or self._min))
        while True:
            value = self.fix(
                random.random() * full_range + (minimum or self._min), dividable_by
            )
            while value < (minimum or self._min):
                value += self._step
            while value > (maximum or self._max):
                value -= self._step
            if not zero_allowed and self.is_equal(value, 0.0):
                continue
            return value

    def is_equal(self, value1: float | None, value2: float | None) -> bool:
        return self.format(value1, decimals=8) == self.format(value2, decimals=8)

    def format(self, value: float | None, decimals: int | None = None) -> str:
        if value is None:
            return ""
        if decimals is None:
            decimals = self._decimals
        return f"{value:.{0 if decimals < 1 else decimals}f}"

    def fix(self, value: float, step: float | None = None) -> float:
        if step is None:
            step = self._step
        elif step < self._step:
            raise ValueError(
                f"Step must be greater than or equal to the factory step: {self._step} vs {step}"
            )
        return round(round(value / step) * step, self._decimals)

    def fly_back(self, value: float):
        str_value = self.format(value)
        if value not in self._number_stat:
            self._number_stat[str_value] = 0
        self._number_stat[str_value] += 1

    def print_statistic(self):
        sorted_stat = dict(
            sorted(self._number_stat.items(), key=lambda item: item[1], reverse=True)
        )
        if self._decimals > 0:
            sorted_stat = {key: value for key, value in sorted_stat.items()}
        print("Number stat:", sorted_stat)
