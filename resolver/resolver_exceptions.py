from expression import Expression


class ExpressionResolverException(Exception):
    def __init__(
        self,
        message: str = "Expression resolver exception",
        expression: Expression | None = None,
        parent: Exception | None = None,
    ):
        super().__init__(f"{message} (expression={expression}, parent={parent})")
        self._parent = parent


class ExpressionResolverNotResolvable(ExpressionResolverException):
    def __init__(
        self,
        message: str = "Expression is not resolvable",
        expression: Expression | None = None,
        parent: Exception | None = None,
    ):
        super().__init__(message, expression=expression, parent=parent)


class ExpressionResolverMaybeNotResolvable(ExpressionResolverException):
    def __init__(
        self,
        message: str = "Expression is maybe not resolvable",
        expression: Expression | None = None,
        parent: Exception | None = None,
    ):
        super().__init__(message, expression=expression, parent=parent)
