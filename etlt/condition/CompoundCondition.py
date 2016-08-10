"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
from etlt.condition.Condition import Condition


class CompoundCondition(Condition):
    """
    Abstract parent class for conditions with one or more child conditions.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        self._conditions = []
        """
        The list of conditions of this compound condition.

        :type: list[gdwh.map.Condition.Condition]
        """

    # ------------------------------------------------------------------------------------------------------------------
    def append_condition(self, condition):
        """
        Appends a child condition to the list of conditions of this compound condition.

        :param gdwh.map.Condition.Condition condition: The child conditions.
        """
        self._conditions.append(condition)

# ----------------------------------------------------------------------------------------------------------------------
