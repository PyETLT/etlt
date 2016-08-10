"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
from etlt.condition.SimpleCondition import SimpleCondition


class TrueCondition(SimpleCondition):
    """
    A true condition always evaluates to True.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row):
        """
        Always returns true.

        :param dict row: The row, ignored.

        :rtype: True
        """
        return True

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def scheme(self):
        """
        Returns 'true'.

        :rtype: str
        """
        return 'true'

# ----------------------------------------------------------------------------------------------------------------------
