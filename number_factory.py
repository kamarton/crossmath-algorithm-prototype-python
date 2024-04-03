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
        self._decimals = NumberFactory._get_decimals_from_step(step)

    @staticmethod
    def _get_decimals_from_step(step: float) -> int:
        str_step = ("%.10f" % step).rstrip("0")
        if "." in str_step:
            return len(str_step.split(".")[1])
        return 0

    def get_step(self) -> float:
        return self._step

    def get_minimum(self) -> float:
        return self._min

    def get_maximum(self) -> float:
        return self._max

    def get_decimals(self) -> int:
        return self._decimals

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
                a = int(dividable_by * 10**self._decimals)
                b = int(self._step * 10**self._decimals)
                if a % b != 0:
                    raise ValueError(
                        f"Dividable by must be dividable by step: {dividable_by} vs {self._step}"
                    )
        full_range = abs((maximum or self._max) - (minimum or self._min))
        while True:
            value = self.fix(
                random.random() * full_range + (minimum or self._min), dividable_by
            )
            while value < (minimum or self._min):
                value += self._step
            while value > (maximum or self._max):
                value -= self._step
            if not zero_allowed and NumberFactory.is_zero(value):
                continue
            return value

    @staticmethod
    def is_zero(value: float | None):
        if value is None:
            return False
        return abs(0.0 - value) < 1e-6

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
