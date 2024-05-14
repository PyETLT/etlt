import abc
from typing import Any, Optional

from etlt.writer.Writer import Writer


class SqlLoaderWriter(Writer):
    """
    Abstract parent class for loading rows to a table in a database using a SQL statement for loading data from file.
    """
    handlers = {}
    """
    The handlers for writing objects as a field to a CSV file.

    :type: dict[str,callable]
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, filename: str, encoding: str = 'utf8'):
        """
        Object constructor.

        :param filename: The destination file for the rows.
        :param encoding: The encoding of the text of the destination file.
        """
        Writer.__init__(self)

        self._filename: str = filename
        """
        The name of the destination file.
        """

        self._encoding: str = encoding
        """
        The encoding of the text in the destination file.
        """

        self._file: Any = None
        """
        The underling file object.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def __enter__(self):
        self._file = open(self._filename, mode='wt', encoding=self._encoding)

    # ------------------------------------------------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_value, traceback):
        self._file.close()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def filename(self) -> str:
        """
        Returns the filename.
        """
        return self._filename

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def encoding(self) -> str:
        """
        Returns the encoding.
        """
        return self._encoding

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_bulk_load_sql(self, table_name: str, partition: Optional[str] = None) -> str:
        """
        Returns a SQL statement for bulk loading the data writen to the destination file into a table.

        :param table_name: The name of the table.
        :param partition: When applicable, the name of the partition in which the data must be loaded.`
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def register_handler(class_name: str, handler: callable) -> None:
        """
        Registers a handler for writing instances of a class as a field to the destination file.

        :param class_name: The name of the class.
        :param handler: The handler. This handler will be called with two arguments: the object which value must be
                        writen to the destination file, the file handler.
        """
        SqlLoaderWriter.handlers[class_name] = handler

    # ------------------------------------------------------------------------------------------------------------------
    def _write_field(self, value: Any):
        """
        Writes a single field to the destination file.

        :param value: The value of the field.
        """
        class_name = str(value.__class__)
        if class_name not in self.handlers:
            raise ValueError('No handler has been registered for class: {0!s}'.format(class_name))
        handler = self.handlers[class_name]
        handler(value, self._file)

# ----------------------------------------------------------------------------------------------------------------------
