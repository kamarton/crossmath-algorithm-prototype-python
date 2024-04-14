from number_helper import (
    number_is_zero,
    number_is_equal,
    number_fix,
    number_precision_decimals,
)


def test_is_zero():
    assert number_is_zero(0.0)
    assert not number_is_zero(0.1)
    assert not number_is_zero(-0.1)
    assert not number_is_zero(1.0)
    assert not number_is_zero(-1.0)


def test_is_equal():
    assert number_is_equal(0.0, 0.0)
    assert number_is_equal(-0.0001, -0.0001)
    assert not number_is_equal(0.0001, -0.0001)
    assert not number_is_equal(0.0001, 0.00011)
    # out of precision
    assert number_is_equal(0.0000001, 0.0000002)


def test_fix():
    assert number_fix(1 / 3) == 0.333333
    # out of precision
    less_than_precision = 4 * pow(10, -(number_precision_decimals + 1))
    assert number_fix(less_than_precision) == 0.0
