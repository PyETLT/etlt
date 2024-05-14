import re
from typing import Any, Dict

from etlt.condition.SimpleCondition import SimpleCondition


class RegularExpressionCondition(SimpleCondition):
    """
    A regular expression condition matches a field in the row against a regular expression expression.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row: Dict[str, Any]) -> bool:
        """
        Returns True if the field matches the regular expression of this simple condition. Returns False otherwise.

        :param row: The row.
        """
        if re.search(self._expression, row[self._field]):
            return True

        return False

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def scheme(self) -> str:
        """
        Returns 're'.
        """
        return 're'

# ----------------------------------------------------------------------------------------------------------------------
