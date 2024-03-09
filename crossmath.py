import random
import time
from enum import Enum
from typing import Tuple, List

from table import Table, Cell


class Operators(Enum):
    ADD = '+'
    SUB = '-'
    # MUL = '*'
    # DIV = '/'
    EQ = '='

    @staticmethod
    def get_operators_without_eq() -> list:
        # return [Operators.ADD, Operators.SUB, Operators.MUL, Operators.DIV]
        return [Operators.ADD, Operators.SUB]

    def __str__(self):
        return self.value


class CrossMath:
    def __init__(self, t: Table):
        self.table = t

    @staticmethod
    def _get_random_cell_for_next(cells: List[Cell]) -> Tuple[Cell, int, int]:
        if len(cells) == 0:
            raise ValueError('cells length must be greater than 0')
        start_time = time.time()
        counter = 0
        while True:
            counter += 1
            if time.time() - start_time > 0.005:
                raise Exception('timeout: ', time.time() - start_time, 'counter: ', counter)
            cells_is_empty = len(cells) == 0
            cell_operand = Cell(0, 0) if cells_is_empty else random.choice(cells)
            return cell_operand, cell_operand.get_x(), cell_operand.get_y()

    @staticmethod
    def _is_valid_operand(operand: int) -> bool:
        return operand >= 0

    @staticmethod
    def _gen_random_operand() -> int:
        return random.randint(1, 9)

    @staticmethod
    def _is_operand(value) -> bool:
        return value is int

    @staticmethod
    def _is_operator(value) -> bool:
        return value is Operators

    def _gen_expression(self, values: list) -> list | None:
        if len(values) > 5:
            raise ValueError('values length must be exactly 5')
        while True:
            if all([value is None for value in values]):
                result = [
                    self._gen_random_operand(),
                    random.choice(Operators.get_operators_without_eq()),
                    self._gen_random_operand(),
                    Operators.EQ,
                ]
                operand3 = eval(f'{result[0]}{result[1]}{result[2]}')
                if self._is_valid_operand(operand3):
                    result.append(operand3)
                    return result
            elif (values[0] is None or self._is_operand(values[0])) and \
                    (values[1] is None or (
                            self._is_operator(values[1]) and values[1] in Operators.get_operators_without_eq())) and \
                    (values[2] is None or self._is_operand(values[2])) and \
                    (values[3] is None or values[3] is Operators.EQ) and \
                    (values[4] is None or self._is_operand(values[4])):
                print('values OK:', values)
                has_op1 = values[0] is not None
                has_opr1 = values[1] is not None
                has_op2 = values[2] is not None
                has_op3 = values[4] is not None
                if not has_op3:
                    # result is not available
                    while True:
                        result = values[:]
                        print('RESULT', result)
                        if not has_op1:
                            result[0] = self._gen_random_operand()
                        if not has_opr1:
                            result[1] = random.choice(Operators.get_operators_without_eq())
                        if not has_op2:
                            result[2] = self._gen_random_operand()
                        result[3] = Operators.EQ
                        result[4] = eval(f'{result[0]}{result[1]}{result[2]}')
                        if self._is_valid_operand(result[4]):
                            return result
                else:
                    # result is available
                    pass

            else:
                # print('values not usable:', values)
                pass
            return None

    def _get_values_for_expression(self, x: int, y: int) -> list[list]:
        result = []
        for o in range(-4, 1):
            values = [[x + 0, y], [1, 0]]
            for i in range(5):
                values.append(self.table.get_cell_value(x + i + o, y))
            result.append(values)
        for o in range(-4, 1):
            values = [[x, y + o], [0, 1]]
            for i in range(5):
                values.append(self.table.get_cell_value(x, y + i + o))
            result.append(values)
        return result

    def generate(self):
        start_time = time.time()
        self.table.clear()
        cells = [self.table.get_cell(0, 0)]
        while True:
            # self.table.print()
            cell_start, x, y = self._get_random_cell_for_next(cells)
            values_list = self._get_values_for_expression(x, y)
            # print('values_list:', values_list)
            random.shuffle(values_list)
            pos = None
            direction = None
            output = None
            for values in values_list:
                pos = values.pop(0)
                direction = values.pop(0)
                output = self._gen_expression(values)
                if output is None:
                    continue
                # TODO cell margin check
                # print(output)
                break
            if output is None:
                cells.remove(cell_start)
                continue

            x = pos[0]
            y = pos[1]
            for i, v in enumerate(output):
                cell = self.table.get_cell(x, y)
                cell.set_value(v)
                cells.append(cell)
                x += direction[0]
                y += direction[1]

            print('time: ', time.time() - start_time)

    def print(self):
        self.table.print()
