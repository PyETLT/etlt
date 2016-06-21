"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import abc


class Writer:
    """
    Abstract parent class for writing transformed, parked, or ignored rows.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def put_row(self, row):
        """
        Writes a row to the designation.

        :param list row: The row.

        :rtype: None
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
