import random
from typing import Tuple, List

WIDTH = 10
HEIGHT = 8
OPERATORS = {
    '+': '-',
    '-': '+',
    '*': '/',
    '/': '*',
}


class TableCell:
    def __init__(self, x: int, y: int, value=None):
        self._value = value
        self._is_operator: bool = False
        self._is_operand: bool = False
        self._x: int = x
        self._y: int = y

    def set_value(self, value):
        self._value = value
        self._is_operand = False
        self._is_operator = False

    def set_operator(self, operation):
        self.set_value(operation)
        self._is_operator = True

    def is_operation(self) -> bool:
        return self._is_operator

    def set_operand(self, operand):
        self.set_value(operand)
        self._is_operand = True

    def is_operand(self) -> bool:
        return self._is_operand

    def is_not_empty(self) -> bool:
        return self._value is not None

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def __str__(self):
        if self._value is None:
            value = '_'
        else:
            value = str(self._value)
        return value

    def __repr__(self):
        x = str(self._x).rjust(2, '0')
        y = str(self._y).rjust(2, '0')
        if self._value is None:
            value = '  '
        else:
            value = str(self._value).rjust(2, ' ')
        return f'[{x},{y}]({value})'


class TableLine:
    def __init__(self, cells: list[TableCell]):
        self._cells = cells
        self._x = cells[0].get_x()
        self._y = cells[0].get_y()

    def get_y(self) -> int:
        return self._y

    def get_x(self) -> int:
        return self._x

    def get_cells(self, offset: int = 0, limit: int = None) -> list[TableCell]:
        if limit is None:
            limit = len(self._cells)
        return self._cells[offset:offset + limit]

    def __str__(self):
        return f'{self._cells}'

    def __repr__(self):
        return f'{self._cells}'


class Table:
    def __init__(self, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self._map: list[list[TableCell]] = self._create_map(width, height)
        self._rows: list[TableLine] = self._get_rows()
        self._cols: list[TableLine] = self._get_cols()

    def _get_rows(self) -> List[TableLine]:
        result = []
        for row in range(self._height):
            result.append(TableLine(self._map[row]))
        return result

    def _get_cols(self) -> List[TableLine]:
        result = []
        for col in range(self._width):
            result.append(TableLine([self._map[row][col] for row in range(self._height)]))
        return result

    @staticmethod
    def _create_map(w, h) -> list[list[TableCell]]:
        _map = []
        for row in range(h):
            _row = []
            for col in range(w):
                _row.append(TableCell(col, row))
            _map.append(_row)
        return _map

    def find_not_empty_cells(self) -> List[TableCell]:
        result = []
        for row in self._map:
            for cell in row:
                if cell.is_not_empty():
                    result.append(cell)
        return result

    def print(self):
        for row in self._map:
            print(''.join(str(cell).rjust(3) for cell in row))

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_cell(self, x: int, y: int) -> TableCell:
        return self._map[y][x]

    def get_row(self, row: int) -> TableLine:
        return self._rows[row]

    def get_column(self, column: int) -> TableLine:
        return self._cols[column]


class CrossMath:
    def __init__(self, t: Table, operators: dict):
        self.table = t
        self.operators = operators

    @staticmethod
    def _gen_operands() -> List[int]:
        return [random.Random().randint(1, 9) for _ in range(2)]

    def _gen_operator(self) -> str:
        return random.choice(list(self.operators.keys()))

    def _gen_random_expression(self, operator=None) -> List:
        while True:
            expression = self._gen_random_expression_free(operator)
            if self._is_valid_expression(expression):
                expression[-1] = int(expression[-1])
                return expression

    @staticmethod
    def _is_valid_expression(expression) -> bool:
        result = expression[-1]
        if result <= 0:
            return False
        if result != int(result):
            return False
        return True

    def _gen_random_expression_free(self, operator=None) -> List:
        if operator is None:
            operator = self._gen_operator()
        operands = self._gen_operands()
        result = eval(f'{operands[0]}{operator}{operands[1]}')
        return [operands[0], operator, operands[1], '=', result]

    def _gen_random_cell_and_position(self) -> Tuple[TableLine, int]:
        cells = self.table.find_not_empty_cells()
        if not cells:
            rand_x = random.choice(range(self.table.get_width()))
            rand_y = random.choice(range(self.table.get_height()))
            cell_operand = self.table.get_cell(rand_x, rand_y)
        else:
            cell_operand = random.choice(cells)
        horizontal = random.choice([True, False])
        line = self.table.get_row(cell_operand.get_y()) if horizontal else self.table.get_column(cell_operand.get_x())
        return line, cell_operand.get_x() if horizontal else cell_operand.get_y()

    def generate(self):
        for _ in range(2):
            self.table.print()
            print('--------------------------------------------------------')
            line, offset = self._gen_random_cell_and_position()
            expression = self._gen_random_expression()

            for i, cell in enumerate(line.get_cells(offset, len(expression))):
                if expression[i] in self.operators or expression[i] == '=':
                    cell.set_operator(expression[i])
                else:
                    cell.set_operand(expression[i])


if __name__ == '__main__':
    table = Table(WIDTH, HEIGHT)
    cross_math = CrossMath(table, OPERATORS)
    cross_math.generate()
    table.print()
