"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import abc


class Reader:
    """
    Abstract parent class for reading (directly or indirectly) rows from the source.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        self._row_number = -1
        """
        The row number for identifying the row in the source data.

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def row_number(self):
        """
        Getter for row count.

        :rtype: int
        """
        return self._row_number

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_source_name(self):
        """
        Returns a name for identifying the current source.

        :rtype: str
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def next(self):
        """
        Yields the next row from the source.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
