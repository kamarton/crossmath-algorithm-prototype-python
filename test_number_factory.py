from number_factory import NumberFactory


def test_range_less():
    number_factory = NumberFactory(minimum=1, maximum=10)
    assert number_factory.next(minimum=5, maximum=5) == 5


def test_range_with_step():
    number_factory = NumberFactory(minimum=1, maximum=10)
    result = number_factory.next(minimum=1, maximum=9, dividable_by=2)
    assert result in [2, 4, 6, 8, 10]


def test_range_with_step_and_decimals():
    number_factory = NumberFactory(minimum=1, maximum=10, decimals=1)
    result = number_factory.next(minimum=1, maximum=3, dividable_by=0.7)
    assert result in [
        1.4,
        2.1,
        2.8,
    ]
