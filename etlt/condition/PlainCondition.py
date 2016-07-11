"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
from etlt.condition.SimpleCondition import SimpleCondition


class PlainCondition(SimpleCondition):
    """
    A plain condition matches a field in the row against a plain value.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row):
        """
        Returns True if the fields equals the expression of this simple condition. Returns False otherwise.

        :param dict row: The row.

        :rtype: bool
        """
        return row[self._field] == self._expression

# ----------------------------------------------------------------------------------------------------------------------
