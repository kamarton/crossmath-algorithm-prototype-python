from expression import ExpressionValidator, Expression
from number_factory import NumberFactory


class ExpressionResolverBase:

    def __init__(self, validator: ExpressionValidator, number_factory: NumberFactory):
        self._validator = validator
        self._number_factory = number_factory

    def resolve(self, expression: Expression) -> Expression:
        """
        Resolve the expression
        """
        raise NotImplementedError()

    def match(self, expression: Expression) -> bool:
        """
        Check if the resolver can resolve the expression
        """
        raise NotImplementedError()

    def _fix(self, value: float) -> float:
        """
        Fix float value
        """
        return self._number_factory.fix(value)

    def _calculate(self, *args):
        """
        Calculate the expression result
        """
        return self._fix(eval(" ".join(map(str, args))))
