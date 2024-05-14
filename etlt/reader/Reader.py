import abc
import copy
from typing import List, Optional


class Reader(metaclass=abc.ABCMeta):
    """
    Abstract parent class for reading (directly or indirectly) rows from the source.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """

        self._fields: Optional[List[str]] = None
        """
        The mapping from field (columns) names to the column numbers in the CSV files.
        """

        self._row_number: int = -1
        """
        The row number for identifying the row in the source data.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fields(self) -> Optional[List[str]]:
        """
        Getter for fields.
        """
        return copy.copy(self._fields)

    # ------------------------------------------------------------------------------------------------------------------
    @fields.setter
    def fields(self, fields: Optional[List[str]]) -> None:
        """
        Setter for fields. If set to None this reader yields each row from the source as a list. If set to a list of
        field names this reader yields each row from the source as a dictionary using the given field names.

        :param fields: The fields (or columns) that must be read from the source.
        """
        self._fields = fields

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def row_number(self) -> int:
        """
        Getter for row count.
        """
        return self._row_number

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_source_name(self) -> str:
        """
        Returns a name for identifying the current source.
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
