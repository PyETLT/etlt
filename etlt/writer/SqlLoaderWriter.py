"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import abc

from etlt.writer.Writer import Writer


class SqlLoaderWriter(Writer):
    """
    Abstract parent class for loading rows to a table in a database using a SQL statement for loading data from file.
    """
    handlers = {}
    """
    The handlers for writing objects as a field to a CSV file.

    :type dict[str,callable]:
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, filename, encoding='utf8'):
        """
        Object constructor.

        :param str filename: The destination file for the rows.
        :param str encoding: The encoding of the text of the destination file.
        """
        Writer.__init__(self)

        self._filename = filename
        """
        The name of the destination file.

        :type str:
        """

        self._encoding = encoding
        """
        The encoding of the text in the destination file.

        :type str:
        """

        self._file = None
        """
        The underling file object.

        :type T:
        """

    # ------------------------------------------------------------------------------------------------------------------
    def __enter__(self):
        self._file = open(self._filename, mode='wt', encoding=self._encoding)

    # ------------------------------------------------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_value, traceback):
        self._file.close()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_bulk_load_sql(self, table_name):
        """
        Returns a SQL statement for bulk loading the data writen to the destination file into a table.

        :param str table_name: The name of the table.

        :rtype: str
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def register_handler(class_name, handler):
        """
        Registers a handler for writing instances of a class as a field to the destination file.

        :param str class_name: The name of the class.
        :param callable handler: The handler. This handler will be called with two arguments: the object which value
                                 must be writen to the destination file, the file handler.
        """
        SqlLoaderWriter.handlers[class_name] = handler

    # ------------------------------------------------------------------------------------------------------------------
    def _write_field(self, value):
        class_name = str(value.__class__)
        if class_name not in self.handlers:
            raise ValueError('No handler has been registered for class: {0!s}'.format(class_name))
        handler = self.handlers[class_name]
        handler(value, self._file)

# ----------------------------------------------------------------------------------------------------------------------
