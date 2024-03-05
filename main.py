import random

WIDTH = 20
HEIGHT = 20
OPERATORS = ['+', '-', '*', '/']


class TableCell:
    def __init__(self, x: int, y: int, value=None):
        self.value = value
        self.operation = None
        self.x = x
        self.y = y

    def set_value(self, value):
        self.value = value

    def set_operation(self, operation):
        self.set_value(operation)
        self.operation = True

    def is_operation(self):
        return self.operation is True

    def __str__(self):
        if self.value is None:
            value = '_'
        else:
            value = str(self.value)
        return value

    def __repr__(self):
        x = str(self.x).rjust(2, '0')
        y = str(self.y).rjust(2, '0')
        if self.value is None:
            value = '  '
        else:
            value = str(self.value).rjust(2, ' ')
        return f'[{x},{y}]({value})'


class TableLine:
    def __init__(self, cells):
        self.cells = cells
        self.x = cells[0].x
        self.y = cells[0].y

    def __str__(self):
        return f'{self.cells}'

    def __repr__(self):
        return f'{self.cells}'


class Table:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = self._create_map(width, height)
        self.rows = self._get_rows()
        self.cols = self._get_cols()

    def _get_rows(self):
        result = []
        for row in range(self.height):
            result.append(TableLine(self.map[row]))
        return result

    def _get_cols(self):
        result = []
        for col in range(self.width):
            result.append(TableLine([self.map[row][col] for row in range(self.height)]))
        return result

    @staticmethod
    def _create_map(w, h):
        _map = []
        for row in range(h):
            _row = []
            for col in range(w):
                _row.append(TableCell(col, row))
            _map.append(_row)
        return _map

    def print(self):
        for row in self.map:
            print(''.join(str(cell).rjust(3) for cell in row))


class CrossMath:
    def __init__(self, t: Table, operators: list):
        self.table = t
        self.operators = operators

    @staticmethod
    def _gen_operands():
        return [random.Random().randint(1, 9) for _ in range(2)]

    def _gen_operator(self):
        return random.choice(self.operators)

    def _gen_random_expression(self, operator=None):
        while True:
            expression = self._gen_random_expression_free(operator)
            if self._is_valid_expression(expression):
                expression[-1] = int(expression[-1])
                return expression

    @staticmethod
    def _is_valid_expression(expression):
        result = expression[-1]
        if result <= 0:
            return False
        if result != int(result):
            return False
        return True

    def _gen_random_expression_free(self, operator=None):
        if operator is None:
            operator = self._gen_operator()
        operands = self._gen_operands()
        result = eval(f'{operands[0]}{operator}{operands[1]}')
        return [operands[0], operator, operands[1], '=', result]

    def generate(self):
        lines = []
        for i in range(3, self.table.height - 3):
            lines.append(self.table.rows[i])
        for i in range(3, self.table.width - 3):
            lines.append(self.table.cols[i])
        line = random.choice(lines)
        expression = self._gen_random_expression()
        col = random.choice(range(self.table.width - len(expression)))
        for i, cell in enumerate(line.cells[col:col + len(expression)]):
            cell.set_value(expression[i])


if __name__ == '__main__':
    table = Table(WIDTH, HEIGHT)
    cross_math = CrossMath(table, OPERATORS)
    cross_math.generate()
    table.print()
