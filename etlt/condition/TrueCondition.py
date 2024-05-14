from typing import Any, Dict

from etlt.condition.SimpleCondition import SimpleCondition


class TrueCondition(SimpleCondition):
    """
    A true condition always evaluates to True.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row: Dict[str, Any]) -> True:
        """
        Always returns true.

        :param dict row: The row, ignored.
        """
        return True

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def scheme(self) -> str:
        """
        Returns 'true'.
        """
        return 'true'

# ----------------------------------------------------------------------------------------------------------------------
