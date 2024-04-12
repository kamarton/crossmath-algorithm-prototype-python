def number_is_zero(value: float | None):
    if value is None:
        return False
    return abs(0.0 - value) < 1e-6


def number_is_equal(value1: float | None, value2: float | None) -> bool:
    if value1 is None and value2 is None:
        return True
    if value1 is None or value2 is None:
        return False
    return number_is_zero(value1 - value2)


def number_fix(value: float | None) -> float | None:
    if value is None:
        return None
    return round(value, 6)
