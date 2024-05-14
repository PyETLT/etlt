import abc
import copy
from typing import Any, Dict, List


class Writer(metaclass=abc.ABCMeta):
    """
    Abstract parent class for writing rows to a destination.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """

        self._fields: List[str] = []
        """
        The fields (columns) that must be written to the destination.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fields(self) -> List[str]:
        """
        Getter for fields.
        """
        return copy.copy(self._fields)

    # ------------------------------------------------------------------------------------------------------------------
    @fields.setter
    def fields(self, fields: List[str]) -> None:
        """
        Setter for fields.

        :param fields: The fields (or columns) that must be written to the destination.
        """
        self._fields = fields

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def writerow(self, row: Dict[str, Any]) -> None:
        """
        Writes a row to the destination.

        :param row: The row.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def __enter__(self):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
