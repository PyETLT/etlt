"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import abc
import copy


class Writer(metaclass=abc.ABCMeta):
    """
    Abstract parent class for writing rows to a destination.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """

        self._fields = []
        """
        The fields (or columns) that must be written to the destination.

        :type: list[str]
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

        :param list[str] fields: The fields (or columns) that must be written to the destination.
        """
        self._fields = fields

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def writerow(self, row):
        """
        Writes a row to the destination.

        :param dict[str,T] row: The row.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def __enter__(self):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
