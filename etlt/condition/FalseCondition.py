from typing import Any, Dict

from etlt.condition.SimpleCondition import SimpleCondition


class FalseCondition(SimpleCondition):
    """
    A false condition always evaluates to False.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row: Dict[str, Any]) -> False:
        """
        Always returns False.

        :param row: The row, ignored
        """
        return False

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def scheme(self) -> str:
        """
        Returns 'false'.
        """
        return 'false'

# ----------------------------------------------------------------------------------------------------------------------
