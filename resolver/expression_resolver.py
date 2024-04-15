from expression import Expression, ExpressionValidator
from number_factory import NumberFactory
from operator_factory import OperatorFactory
from resolver.resolver_base import ExpressionResolverBase
from resolver.resolver_only_operator_missing import OnlyOperatorMissingResolver
from resolver.resolver_result_is_available import ResultIsAvailableResolver
from resolver.resolver_result_is_none import ResultIsNoneResolver


class ExpressionResolver:
    def __init__(
        self,
        validator: ExpressionValidator,
        number_factory: NumberFactory,
        operator_factory: OperatorFactory,
    ):
        self._validator = validator
        self._number_factory = number_factory
        self._operator_factory = operator_factory
        self._resolvers: list[ExpressionResolverBase] = [
            ResultIsNoneResolver(validator, number_factory, operator_factory),
            OnlyOperatorMissingResolver(validator, number_factory, operator_factory),
            ResultIsAvailableResolver(validator, number_factory, operator_factory),
        ]

    def resolve(self, expression: Expression) -> Expression | None:
        """
        Resolve the expression

        :param expression: The expression to resolve
        :return: The resolved expression
        """
        for resolver in self._resolvers:
            if resolver.match(expression):
                resolved_expression = resolver.resolve(expression)
                self._fly_back(expression, resolved_expression)
                return resolved_expression

    def _fly_back(self, base: Expression, result: Expression):
        """
        Fly back expression parts

        :param base: The base expression
        :param result: The result expression
        """
        if base.operand1 is None:
            self._number_factory.fly_back(result.operand1)
        if base.operand2 is None:
            self._number_factory.fly_back(result.operand2)
        if base.result is None:
            self._number_factory.fly_back(result.result)
        if base.operator is None:
            self._operator_factory.fly_back(result.operator)
