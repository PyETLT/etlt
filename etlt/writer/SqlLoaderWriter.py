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

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_bulk_load_sql(self, table_name):
        """
        Returns a SQL statement for bulk loading the data into a table.

        :param str table_name: The name of the table.

        :rtype: str
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
