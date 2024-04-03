from number_factory import NumberFactory


def eq(a: float, b: float, tolerance: float = 1e-6) -> bool:
    return abs(a - b) < tolerance


def eq_in(a: float, arr: list, tolerance: float = 1e-6) -> bool:
    for b in arr:
        if eq(a, b, tolerance):
            return True
    return False


def test_range_less():
    number_factory = NumberFactory(minimum=1, maximum=10)
    assert eq(number_factory.next(minimum=5, maximum=5), 5)


def test_range_with_dividable_by_2():
    number_factory = NumberFactory(minimum=1, maximum=10)
    result = number_factory.next(minimum=1, maximum=9, dividable_by=2)
    assert eq_in(result, [2, 4, 6, 8])


def test_range_with_dividable_by_step_0_1():
    """
    0.1 step with dividable by 0.7
    """
    number_factory = NumberFactory(minimum=1, maximum=10, step=0.1)
    result = number_factory.next(minimum=1, maximum=3, dividable_by=0.7)
    assert eq_in(result, [1.4, 2.1, 2.8])


def test_range_with_dividable_by_step_0_2():
    """
    0.2 step with dividable by 0.8
    """
    number_factory = NumberFactory(minimum=1, maximum=10, step=0.2)
    result = number_factory.next(minimum=1, maximum=3, dividable_by=0.8)
    assert eq_in(result, [1.6, 2.4])


def test_fix_0_2():
    """
    0.2 step with fix
    """
    number_factory = NumberFactory(step=0.2)
    assert eq(number_factory.fix(1.405), 1.4)
    assert eq(number_factory.fix(1.4), 1.4)
    assert eq(number_factory.fix(1.5), 1.6)
    assert eq(number_factory.fix(1.6), 1.6)
    assert eq(number_factory.fix(-1.6), -1.6)
    assert eq(number_factory.fix(-1.5), -1.6)


def test_decimals():
    number_factory = NumberFactory(step=1.0)
    assert number_factory.get_decimals() == 0
    number_factory = NumberFactory(step=0.1)
    assert number_factory.get_decimals() == 1
    number_factory = NumberFactory(step=0.01)
    assert number_factory.get_decimals() == 2
    number_factory = NumberFactory(step=0.2)
    assert number_factory.get_decimals() == 1
    number_factory = NumberFactory(step=0.25)
    assert number_factory.get_decimals() == 2
    number_factory = NumberFactory(step=1)
    assert number_factory.get_decimals() == 0
    number_factory = NumberFactory(step=10)
    assert number_factory.get_decimals() == 0
    number_factory = NumberFactory(step=100)
    assert number_factory.get_decimals() == 0


def test_is_zero():
    assert NumberFactory.is_zero(0.0)
    assert not NumberFactory.is_zero(0.1)
    assert not NumberFactory.is_zero(-0.1)
    assert not NumberFactory.is_zero(1.0)
    assert not NumberFactory.is_zero(-1.0)
