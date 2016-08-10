"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
from etlt.condition.SimpleCondition import SimpleCondition


class FalseCondition(SimpleCondition):
    """
    A false condition always evaluates to False.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row):
        """
        Always returns False.

        :param dict row: The row, ignored

        :rtype: False
        """
        return False

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def scheme(self):
        """
        Returns 'false'.

        :rtype: str
        """
        return 'false'

# ----------------------------------------------------------------------------------------------------------------------
