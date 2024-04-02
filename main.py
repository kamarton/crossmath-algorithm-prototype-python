import os

from crossmath import CrossMath
from expression_map import ExpressionMap
from number_factory import NumberFactory

WIDTH = int(os.environ.get("WIDTH", 20))
HEIGHT = int(os.environ.get("HEIGHT", 20))
NUMBER_FACTORY_MIN = float(os.environ.get("NUMBER_FACTORY_MIN", 0.1))
NUMBER_FACTORY_MAX = float(os.environ.get("NUMBER_FACTORY_MAX", 8.0))
NUMBER_FACTORY_STEP = float(os.environ.get("NUMBER_FACTORY_STEP", 0.5))

if __name__ == "__main__":
    exp_map = ExpressionMap(width=WIDTH, height=HEIGHT)
    number_factory = NumberFactory(
        minimum=NUMBER_FACTORY_MIN,
        maximum=NUMBER_FACTORY_MAX,
        step=NUMBER_FACTORY_STEP,
    )
    cross_math = CrossMath(exp_map=exp_map, number_factory=number_factory)
    # try:
    cross_math.generate()
    cross_math.print()
    number_factory.print_statistic()
    # except Exception as e:
    #     print(e)
    # finally:
    #     cross_math.print()
