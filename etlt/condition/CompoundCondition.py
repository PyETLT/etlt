from abc import ABC
from typing import List

from etlt.condition.Condition import Condition


class CompoundCondition(Condition, ABC):
    """
    Abstract parent class for conditions with one or more child conditions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        self._conditions: List[Condition] = []
        """
        The list of conditions of this compound condition.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def append_condition(self, condition: Condition) -> None:
        """
        Appends a child condition to the list of conditions of this compound condition.

        :param condition: The child conditions.
        """
        self._conditions.append(condition)

# ----------------------------------------------------------------------------------------------------------------------
