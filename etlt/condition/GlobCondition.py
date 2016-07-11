"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import fnmatch

from etlt.condition.SimpleCondition import SimpleCondition


class GlobCondition(SimpleCondition):
    """
    A glob condition matches a field in the row against a glob expression.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row):
        """
        Returns True if the field matches the glob expression of this simple condition. Returns False otherwise.

        :param dict row: The row.

        :rtype: bool
        """
        return fnmatch.fnmatchcase(row[self._field], self._expression)

# ----------------------------------------------------------------------------------------------------------------------
