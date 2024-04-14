from enum import Enum
from typing import TypeVar

from number_helper import number_is_zero, number_is_equal

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
        """
        Returns a list of operators without the equal operator.
        """
        return [Operator.ADD, Operator.SUB, Operator.MUL, Operator.DIV]

    def __str__(self):
        return self.value


class Expression:

    SUPPORTED_LENGTHS = (5,)

    def __init__(self):
        self.operator: Operator | None = None
        self.operand1: float | None = None
        self.operand2: float | None = None
        self.result: float | None = None
        self._length: int = 5

    def values(self) -> list:
        return [self.operand1, self.operator, self.operand2, Operator.EQ, self.result]

    def is_empty(self) -> bool:
        """
        Returns True if expression is fully empty
        """
        return (
            self.operator is None
            and self.operand1 is None
            and self.operand2 is None
            and self.result is None
        )

    @staticmethod
    def from_list(values: list) -> Exp:
        if len(values) not in Expression.SUPPORTED_LENGTHS:
            raise ValueError(
                f"Invalid values ({len(values)} not in {Expression.SUPPORTED_LENGTHS})"
            )
        expression = Expression()
        if values[0] is not None and not isinstance(values[0], float):
            raise ValueError("Invalid values (operand1)")
        expression.operand1 = values[0]
        if (
            values[1] is not None
            and values[1] not in Operator.get_operators_without_eq()
        ):
            raise ValueError("Invalid values (operator)")
        expression.operator = values[1]
        if values[2] is not None and not isinstance(values[2], float):
            raise ValueError("Invalid values (operand2)")
        expression.operand2 = values[2]
        if values[3] is not None and values[3] != Operator.EQ:
            raise ValueError("Invalid values (EQ)")
        if values[4] is not None and not isinstance(values[4], float):
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
        """
        Returns the length of the expression

        :return: The length of the expression
        """
        return self._length

    def is_match(self, exp: Exp, none_allowed: bool = True) -> bool:
        if not none_allowed:
            raise ValueError("Not supported")
        return (
            (
                self.operand1 is None
                or exp.operand1 is None
                or number_is_equal(self.operand1, exp.operand1)
            )
            and (
                self.operator is None
                or exp.operator is None
                or self.operator == exp.operator
            )
            and (
                self.operand2 is None
                or exp.operand2 is None
                or number_is_equal(self.operand2, exp.operand2)
            )
            and (
                self.result is None
                or exp.result is None
                or number_is_equal(self.result, exp.result)
            )
        )


class ExpressionValidator:
    def __init__(
        self,
        minimum: float = 0.0,
        maximum: float = 100.0,
    ):
        self._minimum: float = minimum
        self._maximum: float = maximum

    @staticmethod
    def _is_float(value) -> bool:
        return isinstance(value, float)

    def validate(self, expression: Expression) -> bool:
        if (
            expression.operator is None
            or expression.operand1 is None
            or expression.operand2 is None
            or expression.result is None
        ):
            return False
        if (
            not self._is_float(expression.operand1)
            or not self._is_float(expression.operand2)
            or not self._is_float(expression.result)
        ):
            return False
        if not self._check_range(expression.operand1) or not self._is_float(
            expression.operand1
        ):
            return False
        if not self._check_range(expression.operand2) or not self._is_float(
            expression.operand2
        ):
            return False
        if not self._check_range(expression.result):
            return False
        if expression.operator == Operator.DIV and number_is_zero(expression.operand2):
            return False
        return number_is_equal(
            eval(f"{expression.operand1} {expression.operator} {expression.operand2}"),
            expression.result,
        )

    def _check_range(self, value: float) -> bool:
        return self._minimum <= value <= self._maximum


def is_zero_division(operator: Operator, operand2: float) -> bool:
    return operator == Operator.DIV and number_is_zero(operand2)
