"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
from etlt.condition.SimpleConditionFactory import SimpleConditionFactory

from etlt.condition.Condition import Condition


class InListCondition(Condition):
    """
    A list condition matches a single field against a list of conditions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, field):
        """
        Object contructor.

        :param str field: The name of the field in the row that must be match against the expression.
        """
        self._field = field
        """
        The name of the field in the row that must be match against the list of values.

        :type: str
        """

        self._values = list()
        """
        The list of values of plain conditions.

        :type: list[str]
        """

        self._conditions = list()
        """
        The list of other conditions.

        :type: list[etlt.condition.SimpleCondition.SimpleCondition]
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def field(self):
        """
        Getter for field.

        :rtype: str
        """
        return self._field

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def values(self):
        """
        Getter for values.

        :rtype: list[str]
        """
        return self._values

    # ------------------------------------------------------------------------------------------------------------------
    def populate_values(self, rows, field):
        """
        Populates the filter values of this filter using list of rows.

        :param list[dict[str,T]] rows: The row set.
        :param str field: The field name.
        """
        self._values.clear()
        for row in rows:
            condition = SimpleConditionFactory.create_condition(self._field, row[field])
            if condition.scheme == 'plain':
                self._values.append(condition.expression)
            else:
                self._conditions.append(condition)

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row):
        """
        Returns True if the field is in the list of conditions. Returns False otherwise.

        :param dict row: The row.

        :rtype: bool
        """
        if row[self._field] in self._values:
            return True

        for condition in self._conditions:
            if condition.match(row):
                return True

        return False

# ----------------------------------------------------------------------------------------------------------------------
