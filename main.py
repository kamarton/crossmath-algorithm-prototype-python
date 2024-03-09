from crossmath import CrossMath
from table import Table

if __name__ == '__main__':
    cross_math = CrossMath(Table())
    try:
        cross_math.generate()
    except Exception as e:
        print(e)
    finally:
        cross_math.print()
