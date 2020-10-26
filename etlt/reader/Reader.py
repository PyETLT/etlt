import abc
import copy


class Reader(metaclass=abc.ABCMeta):
    """
    Abstract parent class for reading (directly or indirectly) rows from the source.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        self._fields = None
        """
        The fields (or columns) that this reader will read from the source.

        :type: list[str]|None
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

        :rtype: list[str]|None
        """
        return copy.copy(self._fields)

    # ------------------------------------------------------------------------------------------------------------------
    @fields.setter
    def fields(self, fields):
        """
        Setter for fields. If set to None this reader yields each row from the source as a list. If set to a list of
        field names this reader yields each row from the source as a dictionary using the given field names.

        :param list[str]|None fields: The fields (or columns) that must be read from the source.
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
