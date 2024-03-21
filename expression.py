from enum import Enum
from typing import TypeVar

import pandas

Exp = TypeVar("Exp", bound="Expression")
Opr = TypeVar("Opr", bound="Operator")


class Operator(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    EQ = "="

    @staticmethod
    def get_operators_without_eq() -> list:
        return [Operator.ADD, Operator.SUB, Operator.MUL, Operator.DIV]

    def __str__(self):
        return self.value


class Expression:

    SUPPORTED_LENGTHS = (5,)

    def __init__(self):
        self.operator: Operator | None = None
        self.operand1: int | None = None
        self.operand2: int | None = None
        self.result: int | None = None
        self._length: int = 5

    def values(self) -> list:
        return [self.operand1, self.operator, self.operand2, Operator.EQ, self.result]

    def is_empty(self) -> bool:
        return (
            self.operator is None
            and self.operand1 is None
            and self.operand2 is None
            and self.result is None
        )

    @staticmethod
    def from_str(exp: str) -> Exp:
        values = exp.split()
        result = []
        for i in range(0, len(values)):
            if values[i] == "?":
                result.append(None)
            elif i % 2 == 0:
                result.append(int(values[i]))
            else:
                result.append(Operator(values[i]))
        return Expression.from_values(result)

    @staticmethod
    def from_values(values: list) -> Exp:
        if len(values) not in Expression.SUPPORTED_LENGTHS:
            raise ValueError(
                f"Invalid values ({len(values)} not in {Expression.SUPPORTED_LENGTHS})"
            )
        expression = Expression()
        if values[0] is not None and not isinstance(values[0], int):
            raise ValueError("Invalid values (operand1)")
        expression.operand1 = values[0]
        if (
            values[1] is not None
            and values[1] not in Operator.get_operators_without_eq()
        ):
            raise ValueError("Invalid values (operator)")
        expression.operator = values[1]
        if values[2] is not None and not isinstance(values[2], int):
            raise ValueError("Invalid values (operand2)")
        expression.operand2 = values[2]
        if values[3] is not None and values[3] != Operator.EQ:
            raise ValueError("Invalid values (EQ)")
        if values[4] is not None and not isinstance(values[4], int):
            raise ValueError("Invalid values (result)")
        expression.result = values[4]
        return expression

    def clone(self) -> Exp:
        expression = Expression()
        expression.operand1 = self.operand1
        expression.operator = self.operator
        expression.operand2 = self.operand2
        expression.result = self.result
        return expression

    def __str__(self):
        return f"{self.operand1} {self.operator} {self.operand2} = {self.result}"

    def get_length(self) -> int:
        return self._length


class ExpressionValidator:
    def __int__(self):
        pass

    @staticmethod
    def _is_integer(value) -> bool:
        return value == int(value)

    def validate(self, expression: Expression) -> bool:
        if (
            expression.operator is None
            or expression.operand1 is None
            or expression.operand2 is None
            or expression.result is None
        ):
            return False
        if (
            expression.operand1 < 1
            or expression.operand1 > 100
            or not self._is_integer(expression.operand1)
        ):
            return False
        if (
            expression.operand2 < 1
            or expression.operand2 > 100
            or not self._is_integer(expression.operand2)
        ):
            return False
        if expression.result < 1 or expression.result > 100:
            return False
        if not self._is_integer(expression.result):
            return False
        return (
            eval(f"{expression.operand1} {expression.operator} {expression.operand2}")
            == expression.result
        )
