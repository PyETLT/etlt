import fnmatch
from typing import Any, Dict

from etlt.condition.SimpleCondition import SimpleCondition


class GlobCondition(SimpleCondition):
    """
    A glob condition matches a field in the row against a glob expression.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row: Dict[str, Any]) -> bool:
        """
        Returns whether the field matches the glob expression of this simple condition.

        :param dict row: The row.
        """
        return fnmatch.fnmatchcase(row[self._field], self._expression)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def scheme(self) -> str:
        """
        Returns 'glob'.
        """
        return 'glob'

# ----------------------------------------------------------------------------------------------------------------------
