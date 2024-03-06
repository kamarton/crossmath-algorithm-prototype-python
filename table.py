from typing import List


class Cell:
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

    def set_operator(self, operator):
        self.set_value(operator)
        self._is_operator = True

    def is_operator(self) -> bool:
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
        x = str(self._x).rjust(2, ' ')
        y = str(self._y).rjust(2, ' ')
        if self._value is None:
            value = '   '
        else:
            value = str(self._value).center(3, ' ')
        return f'({x} x {y}) | {value} |'


class Table:
    def __init__(self):
        self._cells: list[Cell] = list()
        self._min_x: int = 0
        self._min_y: int = 0
        self._max_x: int = 0
        self._max_y: int = 0

    def find_not_empty_cells(self) -> List[Cell]:
        result = []
        for cell in self._cells:
            if cell.is_not_empty():
                result.append(cell)
        return result

    def get_cell(self, x: int, y: int, empty_cell: bool = True) -> Cell | None:
        for cell in self._cells:
            if cell.get_x() == x and cell.get_y() == y:
                return cell
        return TableCell(self, x, y) if empty_cell else None

    def print(self):
        for y in range(self.get_min_y(), self.get_max_y() + 1):
            row = []
            for x in range(self.get_min_x(), self.get_max_x() + 1):
                cell = self.get_cell(x, y)
                row.append(cell)
            print(row)

    def get_min_x(self) -> int:
        return self._min_x

    def get_min_y(self) -> int:
        return self._min_y

    def get_max_x(self) -> int:
        return self._max_x

    def get_max_y(self) -> int:
        return self._max_y

    def add_cell(self, cell: Cell):
        x = cell.get_x()
        y = cell.get_y()
        if self.get_cell(x, y, False) is not None:
            raise ValueError('Cell already exists')
        self._min_x = min(self._min_x, x)
        self._min_y = min(self._min_y, y)
        self._max_x = max(self._max_x, x)
        self._max_y = max(self._max_y, y)
        self._cells.append(cell)


class TableCell(Cell):
    def __init__(self, table: Table, x: int, y: int):
        super().__init__(x, y)
        self._table = table
        self._added_to_table: bool = False

    def set_value(self, value):
        if not self._added_to_table:
            self._table.add_cell(self)
            self._added_to_table = True
        super().set_value(value)
