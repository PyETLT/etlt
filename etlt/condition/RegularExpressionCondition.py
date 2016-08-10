"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import re

from etlt.condition.SimpleCondition import SimpleCondition


class RegularExpressionCondition(SimpleCondition):
    """
    A regular expression condition matches a field in the row against a regular expression expression.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row):
        """
        Returns True if the field matches the regular expression of this simple condition. Returns False otherwise.

        :param dict row: The row.

        :rtype: bool
        """
        if re.search(self._expression, row[self._field]):
            return True

        return False

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def scheme(self):
        """
        Returns 're'.

        :rtype: str
        """
        return 're'

# ----------------------------------------------------------------------------------------------------------------------
