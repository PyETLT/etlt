import abc


class Condition(metaclass=abc.ABCMeta):
    """
    An abstract parent class for conditions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def match(self, row):
        """
        Returns True if the row matches this condition. Returns False otherwise.

        :param dict row: The row.

        :rtype: bool
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
