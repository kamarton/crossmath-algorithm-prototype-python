import math
import random
import time


class RandomGenerator:
    def __init__(self, seed: int = None):
        self._seed = seed
        self._random = random.Random(seed)

    def next_int(self, maximum: int) -> int:
        return self._random.randint(0, maximum)


class NumberFactory:

    def __init__(
        self,
        minimum: float = 1.0,
        maximum: float = 10.0,
        step: float = 1,
        random_generator: RandomGenerator | None = None,
    ):
        self._number_stat: dict[str, int] = {}
        self._min: float = minimum
        self._max: float = maximum
        if step <= 0:
            raise ValueError("Step must be greater than 0")
        self._step = step
        self._decimals = NumberFactory._get_decimals_from_step(step)
        self._random_generator: RandomGenerator = random_generator or RandomGenerator()

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
        minimum = max(self._min, minimum or self._min)
        maximum = min(self._max, maximum or self._max)
        if minimum > maximum:
            raise ValueError(f"Minimum is greater than maximum: {minimum} > {maximum}")
        if dividable_by is not None:
            if NumberFactory.is_zero(dividable_by):
                dividable_by = self._step
            else:
                dividable_by = abs(dividable_by)
                a = int(dividable_by * 10**self._decimals)
                b = int(self._step * 10**self._decimals)
                if a % b != 0:
                    raise ValueError(
                        f"Dividable by must be dividable by step: {dividable_by} vs {self._step}"
                    )
        else:
            dividable_by = self._step
        minimum_start = math.ceil(minimum / dividable_by) * dividable_by
        maximum_end = math.floor(maximum / dividable_by) * dividable_by
        full_range = abs(maximum_end - minimum_start)
        range_int = int(full_range / dividable_by)
        start_time = time.time()
        if (
            not zero_allowed
            and dividable_by > abs(minimum_start)
            and dividable_by > abs(maximum_end)
        ):
            raise ValueError(
                f"Dividable by / step must be less than minimum or maximum: {dividable_by} vs [{minimum_start}, {maximum_end}]"
            )
        if minimum_start > maximum_end:
            raise ValueError(
                f"Minimum is greater than maximum (modified): {minimum_start} > {maximum_end}"
            )
        max_runtime_sec = 0.1
        while time.time() - start_time < max_runtime_sec:
            random_in_range = self._random_generator.next_int(range_int)
            value = minimum_start + random_in_range * dividable_by
            value_fixed = self.fix(value, dividable_by)
            if not NumberFactory.is_equal(value, self.fix(value, dividable_by)):
                raise RuntimeError(
                    f"Value is not equal to fixed value: {value} vs {value_fixed}"
                )
            if value < minimum_start:
                raise RuntimeError(
                    f"Value is less than minimum: {value} < {minimum_start} minimum={minimum}"
                )
            if value > maximum_end:
                raise RuntimeError(
                    f"Value is greater than maximum: {value} > {maximum_end} maximum={maximum}"
                )
            if not zero_allowed and NumberFactory.is_zero(value):
                continue
            return self.fix(value)
        raise RuntimeError(
            f"Cannot find random value in {max_runtime_sec} second, paramters: minimum={minimum}, maximum={maximum}, dividable_by={dividable_by}, zero_allowed={zero_allowed}"
        )

    @staticmethod
    def is_zero(value: float | None):
        if value is None:
            return False
        return abs(0.0 - value) < 1e-6

    @staticmethod
    def is_equal(value1: float | None, value2: float | None) -> bool:
        if value1 is None and value2 is None:
            return True
        if value1 is None or value2 is None:
            return False
        return NumberFactory.is_zero(value1 - value2)

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
        if str_value not in self._number_stat:
            self._number_stat[str_value] = 0
        self._number_stat[str_value] += 1

    def print_statistic(self):
        swapped_stat = {}
        for k, v in self._number_stat.items():
            if v not in swapped_stat:
                swapped_stat[v] = []
            swapped_stat[v].append(float(k))

        print("Number factory statistic:")
        for k in sorted(swapped_stat.keys(), reverse=True):
            v = swapped_stat[k]
            v.sort()
            joined_v = ", ".join(map(str, v))
            print(f"{k:<5} -> {joined_v}")
