import os

from crossmath import CrossMath
from expression_map import ExpressionMap

WIDTH = int(os.environ.get("WIDTH", 20))
HEIGHT = int(os.environ.get("HEIGHT", 20))

if __name__ == "__main__":
    exp_map = ExpressionMap(width=WIDTH, height=HEIGHT)
    cross_math = CrossMath(exp_map=exp_map)
    # try:
    cross_math.generate()
    cross_math.print()
    # except Exception as e:
    #     print(e)
    # finally:
    #     cross_math.print()
