import parametrize_from_file

from expression import Expression, ExpressionValidator
from expression_resolver import ExpressionResolver
from number_factory import NumberFactory


@parametrize_from_file
def test_expression_resolver(expression: str, expect: str):
    number_factory = NumberFactory(minimum=1, maximum=10)
    resolver = ExpressionResolver(
        validator=ExpressionValidator(number_factory=number_factory),
        number_factory=number_factory,
    )
    parsed_expression = Expression.from_str(expression)
    expected_expression = Expression.from_str(expect)
    resolved_expression = resolver.resolve(parsed_expression)
    assert resolved_expression is not None
    assert resolved_expression.operand1 == expected_expression.operand1
    assert resolved_expression.operator == expected_expression.operator
    assert resolved_expression.operand2 == expected_expression.operand2
    assert resolved_expression.result == expected_expression.result
