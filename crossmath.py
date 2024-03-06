import random
import time
from typing import Tuple, List

from table import Table


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

    def _get_random_cell_for_next(self) -> Tuple[int, int, int, int]:
        start_time = time.time()
        counter = 0
        cells = self.table.find_not_empty_cells()
        if len(cells) == 0:
            cells = [self.table.get_cell(0, 0)]
        while True:
            counter += 1
            if time.time() - start_time > 0.005:
                raise Exception('timeout: ', time.time() - start_time, 'counter: ', counter)
            cell_operand = random.choice(cells)
            directions = []
            if self.table.get_cell(cell_operand.get_x() + 1, cell_operand.get_y()).is_not_empty() is False:
                directions.append((1, 0))
            if self.table.get_cell(cell_operand.get_x() - 1, cell_operand.get_y()).is_not_empty() is False:
                directions.append((-1, 0))
            if self.table.get_cell(cell_operand.get_x(), cell_operand.get_y() + 1).is_not_empty() is False:
                directions.append((0, 1))
            if self.table.get_cell(cell_operand.get_x(), cell_operand.get_y() - 1).is_not_empty() is False:
                directions.append((0, -1))

            if len(directions) == 0:
                cells.remove(cell_operand)
                continue
            direction = random.choice(directions)
            return cell_operand.get_x(), cell_operand.get_y(), direction[0], direction[1]

    def generate(self):
        start_time = time.time()
        for _ in range(20):
            x, y, xadd, yadd = self._get_random_cell_for_next()
            expression = self._gen_random_expression()

            for expression_part in expression:
                cell = self.table.get_cell(x, y)
                cell.set_value(expression_part)
                x += xadd
                y += yadd
            print('time: ', time.time() - start_time)

    def print(self):
        self.table.print()
