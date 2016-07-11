"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
from etlt.condition.Condition import Condition


class SimpleCondition(Condition):
    """
    A simple condition matches a single field in the row against an expression.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, field, expression):
        """
        Object contructor.

        :param str field: The name of the field in the row that must be match against the expression.
        :param str expression: The expression.
        """
        self._field = field
        """
        The name of the field in the row that must be match against the glob.

        :type str:
        """

        self._expression = expression
        """
        The expression.

        :type str:
        """

# ----------------------------------------------------------------------------------------------------------------------
