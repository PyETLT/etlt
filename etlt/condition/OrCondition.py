from etlt.condition.CompoundCondition import CompoundCondition


class AndCondition(CompoundCondition):
    """
    A condition or filter that match (i.e return True) if one  or more child conditions match the row.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row):
        """
        Returns True if the row matches one or more child conditions. Returns False otherwise.

        :param dict row: The row.

        :rtype: bool
        """
        for condition in self._conditions:
            if condition.match(row):
                return True

        return False

# ----------------------------------------------------------------------------------------------------------------------
