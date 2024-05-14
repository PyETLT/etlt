from typing import Any, Dict, List

from etlt.condition.Condition import Condition
from etlt.condition.SimpleCondition import SimpleCondition
from etlt.condition.SimpleConditionFactory import SimpleConditionFactory


class InListCondition(Condition):
    """
    A list condition matches a single field against a list of conditions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, field: str):
        """
        Object contructor.

        :param str field: The name of the field in the row that must be match against the expression.
        """
        self._field: str = field
        """
        The name of the field in the row that must be match against the list of values.
        """

        self._values: List[str] = list()
        """
        The list of values of plain conditions.
        """

        self._conditions: List[SimpleCondition] = list()
        """
        The list of other conditions.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def field(self) -> str:
        """
        Getter for field.
        """
        return self._field

    # ------------------------------------------------------------------------------------------------------------------
    def populate_values(self, rows: List[Dict[str, Any]], field: str):
        """
        Populates the filter values of this filter using list of rows.

        :param rows: The row set.
        :param field: The field name.
        """
        self._values.clear()
        for row in rows:
            condition = SimpleConditionFactory.create_condition(self._field, row[field])
            if condition.scheme == 'plain':
                self._values.append(condition.expression)
            else:
                self._conditions.append(condition)

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row: Dict[str, Any]) -> bool:
        """
        Returns whether the field is in the list of conditions.

        :param dict row: The row.
        """
        if row[self._field] in self._values:
            return True

        for condition in self._conditions:
            if condition.match(row):
                return True

        return False

# ----------------------------------------------------------------------------------------------------------------------
