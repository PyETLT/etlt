"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import abc
import copy


class Reader:
    """
    Abstract parent class for reading (directly or indirectly) rows from the source.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        self._fields = []
        """
        The fields (or columns) that this reader will read from the source.

        :type: list[str]
        """

        self._row_number = -1
        """
        The row number for identifying the row in the source data.

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fields(self):
        """
        Getter for fields.

        :rtype: list[str]
        """
        return copy.copy(self._fields)

    # ------------------------------------------------------------------------------------------------------------------
    @fields.setter
    def fields(self, fields):
        """
        Setter for fields.

        :param list[str] fields: The fields (or columns) that must be read from the source.
        """
        self._fields = fields

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
