from typing import List
import pandas


class Cell:
    def __init__(self, x: int, y: int, value=None):
        self._value = value
        self._x: int = x
        self._y: int = y

    def set_value(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def is_not_empty(self) -> bool:
        return self._value is not None

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def __repr__(self):
        return '' if self._value is None else str(self._value)


class Table:
    def __init__(self):
        self._cells: list[Cell] = list()
        self._min_x: int = 0
        self._min_y: int = 0
        self._max_x: int = 0
        self._max_y: int = 0

    def get_cell(self, x: int, y: int, empty_cell: bool = True) -> Cell | None:
        for cell in self._cells:
            if cell.get_x() == x and cell.get_y() == y:
                return cell
        return TableCell(self, x, y) if empty_cell else None

    def get_cell_value(self, x: int, y: int) -> int:
        cell = self.get_cell(x, y)
        return cell.get_value() if cell is not None else 0

    def print(self):
        rows = []
        for y in range(self.get_min_y(), self.get_max_y() + 1):
            cols = []
            for x in range(self.get_min_x(), self.get_max_x() + 1):
                cell = self.get_cell(x, y)
                cols.append(cell)
            rows.append(cols)
        df = pandas.DataFrame(rows)
        print(df)

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

    def clear(self):
        self._cells.clear()
        self._min_x = 0
        self._min_y = 0
        self._max_x = 0
        self._max_y = 0


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
