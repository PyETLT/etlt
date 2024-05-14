import abc

from etlt.condition.Condition import Condition


class SimpleCondition(Condition):
    """
    A simple condition matches a single field in the row against an expression.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, field: str, expression: str):
        """
        Object contructor.

        :param field: The name of the field in the row that must be match against the expression.
        :param expression: The expression.
        """
        self._field: str = field
        """
        The name of the field in the row that must be match against the expression.
        """

        self._expression: str = expression
        """
        The expression.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def expression(self) -> str:
        """
        Returns the expression.
        """
        return self._expression

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def field(self) -> str:
        """
        Returns the name of the field in the row that must be match against the expression.
        """
        return self._field

    # ------------------------------------------------------------------------------------------------------------------
    @property
    @abc.abstractmethod
    def scheme(self) -> str:
        """
        Returns the scheme of the simple condition.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
