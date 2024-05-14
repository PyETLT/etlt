from typing import Any, Dict

from etlt.condition.CompoundCondition import CompoundCondition


class AndCondition(CompoundCondition):
    """
    A condition or filter that match (i.e. return True) if one or more child conditions match the row.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row: Dict[str, Any]) -> bool:
        """
        Returns True if the row matches one or more child conditions. Returns False otherwise.

        :param dict row: The row.
        """
        for condition in self._conditions:
            if condition.match(row):
                return True

        return False

# ----------------------------------------------------------------------------------------------------------------------
