from typing import Any, Dict

from etlt.condition.CompoundCondition import CompoundCondition


class AndCondition(CompoundCondition):
    """
    A condition or filter that match (i.e. return True) if all child conditions match the row.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row: Dict[str, Any]) -> bool:
        """
        Returns whether a row matches all child conditions.

        :param row: The row.
        """
        for condition in self._conditions:
            if not condition.match(row):
                return False

        return True

# ----------------------------------------------------------------------------------------------------------------------
