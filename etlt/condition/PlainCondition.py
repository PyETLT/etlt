from typing import Any, Dict

from etlt.condition.SimpleCondition import SimpleCondition


class PlainCondition(SimpleCondition):
    """
    A plain condition matches a field in the row against a plain value.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row: Dict[str, Any]) -> bool:
        """
        Returns True if the fields equals the expression of this simple condition. Returns False otherwise.

        :param row: The row.
        """
        return row[self._field] == self._expression

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def scheme(self) -> str:
        """
        Returns 'plain'.
        """
        return 'plain'

# ----------------------------------------------------------------------------------------------------------------------
