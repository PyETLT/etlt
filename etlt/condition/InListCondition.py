"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
from etlt.condition.Condition import Condition


class InListCondition(Condition):
    """
    A list condition matches a single field against a list of values.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, field, values):
        """
        Object contructor.

        :param str field: The name of the field in the row that must be match against the expression.
        :param list[str] values: The list of values.
        """
        self._field = field
        """
        The name of the field in the row that must be match against the list of values.

        :type: str
        """

        self._values = values
        """
        The list of values.

        :type: list[str]
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
            self._values.append(row[field])

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row):
        """
        Returns True if the field is in the list of values. Returns False otherwise.

        :param dict row: The row.

        :rtype: bool
        """
        return row[self._field] in self._values

# ----------------------------------------------------------------------------------------------------------------------
