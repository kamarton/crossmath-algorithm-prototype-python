from crossmath import CrossMath
from table import Table

WIDTH = 10
HEIGHT = 8
OPERATORS = {
    '+': '-',
    '-': '+',
    '*': '/',
    '/': '*',
}

if __name__ == '__main__':
    cross_math = CrossMath(Table(), OPERATORS)
    cross_math.generate()
    cross_math.print()
