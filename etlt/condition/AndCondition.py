from etlt.condition.CompoundCondition import CompoundCondition


class AndCondition(CompoundCondition):
    """
    A condition or filter that match (i.e return True) if all child conditions match the row.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def match(self, row):
        """
        Returns True if the row matches all child conditions. Returns False otherwise.

        :param dict row: The row.

        :rtype: bool
        """
        for condition in self._conditions:
            if not condition.match(row):
                return False

        return True

# ----------------------------------------------------------------------------------------------------------------------
