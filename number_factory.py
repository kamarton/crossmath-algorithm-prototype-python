import random


class NumberFactory:

    def __init__(self, minimum: float = 1.0, maximum: float = 10.0, decimals: int = 0):
        self._number_stat: dict[str, int] = {}
        self._min: float = minimum
        self._max: float = maximum
        self._decimals: int = decimals

    def next(
        self,
        minimum: float | None = None,
        maximum: float | None = None,
        dividable_by: float | None = None,
        zero_allowed: bool = True,
    ) -> float:
        # TODO add support for negative numbers
        if dividable_by is not None and dividable_by == 0:
            raise ValueError("Step cannot be 0")
        full_range = abs((maximum or self._max) - (minimum or self._min))
        while True:
            value = self.fix(random.random() * full_range + (minimum or self._min))
            if dividable_by is not None:
                value = round(value / dividable_by) * dividable_by
                if value < (minimum or self._min):
                    value += dividable_by
                elif value > (maximum or self._max):
                    value -= dividable_by
                value = self.fix(value)
            if zero_allowed or value != 0:
                return value
            continue

    def is_equal(self, value1: float | None, value2: float | None) -> bool:
        return self.format(value1, decimals=8) == self.format(value2, decimals=8)

    def format(self, value: float | None, decimals: int | None = None) -> str:
        if value is None:
            return ""
        if decimals is None:
            decimals = self._decimals
        return f"{value:.{0 if decimals < 1 else decimals}f}"

    def fix(self, value: float):
        return round(value, self._decimals)

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
