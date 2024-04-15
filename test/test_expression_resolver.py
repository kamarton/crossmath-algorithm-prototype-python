import parametrize_from_file

from expression import Expression, ExpressionValidator
from operator_factory import Operator, OperatorFactory
from resolver.expression_resolver import ExpressionResolver
from number_factory import NumberFactory


def expression_from_str(exp: str) -> Expression:
    values = exp.split()
    if len(values) not in Expression.SUPPORTED_LENGTHS:
        raise ValueError("Not supported expression string")
    result = []
    for i in range(0, len(values)):
        if values[i] == "?":
            result.append(None)
        elif i % 2 == 0:
            result.append(float(values[i]))
        else:
            result.append(Operator(values[i]))
    return Expression.from_list(result)


@parametrize_from_file
def test_expression_resolver(expression: str, expect: str):
    number_factory = NumberFactory(minimum=1.0, maximum=10.0)
    operator_factory = OperatorFactory()
    resolver = ExpressionResolver(
        validator=ExpressionValidator(),
        number_factory=number_factory,
        operator_factory=operator_factory,
    )
    parsed_expression = expression_from_str(expression)
    expected_expression = expression_from_str(expect)
    resolved_expression = resolver.resolve(parsed_expression)
    assert resolved_expression is not None
    assert resolved_expression.operand1 == expected_expression.operand1
    assert resolved_expression.operator == expected_expression.operator
    assert resolved_expression.operand2 == expected_expression.operand2
    assert resolved_expression.result == expected_expression.result
