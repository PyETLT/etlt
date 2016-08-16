"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import copy
import datetime


class Type2Helper:
    """
    A helper class for reference data with date intervals.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, key_start_date, key_end_date, natural_key):
        """
        Object constructor.

        :param str key_start_date: The key of the start date in the rows.
        :param str key_end_date: The key of the end date in the rows.
        :param list[str] natural_key: The keys of the columns that form the natural key.
        """
        self._natural_key = list(natural_key)
        """
        The keys of the columns that form the natural key.

        :type: list[str]
        """

        self._key_end_date = key_end_date
        """
        The key of the end date in the rows.

        :type: str
        """
        self._key_start_date = key_start_date
        """
        The key of the start date in the rows.

        :type: str
        """

        self.rows = dict()
        """
        The data set.

        :type: dict
        """

        self._copy = True
        """
        If set to true a copy will be made from the original rows such that the original rows is not modified.

         :type: bool
        """

        self._date_type = ''
        """
        The type of the date fields.
        - date for datetime.date objects
        - str  for strings in ISO 8601 (YYYY-MM-DD) format
        - int for integers

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _get_natural_key(self, row):
        """
        Returns the natural key in a row.

        :param dict row: The row.

        :rtype: tuple
        """
        ret = list()
        for key in self._natural_key:
            ret.append(row[key])

        return tuple(ret)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _date2int(date):
        """
        Returns an integer representation of a date.

        :param str|datetime.date date: The date.

        :rtype: int
        """
        if isinstance(date, str):
            if date.endswith(' 00:00:00') or date.endswith('T00:00:00'):
                # Ignore time suffix.
                date = date[0:-9]
            tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
            return tmp.toordinal()

        if isinstance(date, datetime.date):
            return date.toordinal()

        if isinstance(date, int):
            return date

        raise ValueError('Unexpected type {0!s}'.format(date.__class__))

    # ------------------------------------------------------------------------------------------------------------------
    def _rows_date2int(self, rows):
        """
        Replaces start and end dates in a row set with their integer representation

        :param list[dict[str,T]] rows: The list of rows.

        :rtype: list[dict[str,T]]
        """
        ret = list()
        for row in rows:
            # Determine the type of dates based on the first start date.
            if not self._date_type:
                self._date_type = self._get_date_type(row[self._key_start_date])

            # Convert dates to integers.
            row[self._key_start_date] = self._date2int(row[self._key_start_date])
            row[self._key_end_date] = self._date2int(row[self._key_end_date])
            ret.append(row)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def _rows_int2date(self, rows):
        """
        Replaces start and end dates in the row set with their integer representation

        :param list[dict[str,T]] rows: The list of rows.
        """
        for row in rows:
            if self._date_type == 'str':
                row[self._key_start_date] = datetime.date.fromordinal(row[self._key_start_date]).isoformat()
                row[self._key_end_date] = datetime.date.fromordinal(row[self._key_end_date]).isoformat()
            elif self._date_type == 'date':
                row[self._key_start_date] = datetime.date.fromordinal(row[self._key_start_date])
                row[self._key_end_date] = datetime.date.fromordinal(row[self._key_end_date])
            elif self._date_type == 'int':
                # Nothing to do.
                pass
            else:
                raise ValueError('Unexpected date type {0!s}'.format(self._date_type))

    # ------------------------------------------------------------------------------------------------------------------
    def _rows_sort(self, rows):
        """
        Returns a list of rows sorted by start and end date.

        :param list[dict[str,T]] rows: The list of rows.

        :rtype: list[dict[str,T]]
        """
        return sorted(rows, key=lambda row: (row[self._key_start_date], row[self._key_end_date]))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_date_type(date):
        """
        Returns the type of a date.

        :param str|datetime.date date: The date.

        :rtype: str
        """
        if isinstance(date, str):
            return 'str'

        if isinstance(date, datetime.date):
            return 'date'

        if isinstance(date, int):
            return 'int'

        raise ValueError('Unexpected type {0!s}'.format(date.__class__))

    # ------------------------------------------------------------------------------------------------------------------
    def enumerate(self, name, start=1):
        """
        Enumerates all rows such that the natural key and the ordinal number are a unique key.

        :param str name: The key holding the ordinal number.
        :param int start: The start of the ordinal numbers. Foreach natural key the first row has this ordinal number.
        """
        for natural_key, rows in self.rows.items():
            rows = self._rows_sort(rows)
            ordinal = start
            for row in rows:
                row[name] = ordinal
                ordinal += 1
            self.rows[natural_key] = rows

    # ------------------------------------------------------------------------------------------------------------------
    def get_rows(self, sort=False):
        """
        Returns the rows of this Type2Helper.

        :param bool sort: If True the rows are sorted by the natural key.
        """
        ret = []
        for _, rows in sorted(self.rows.items()) if sort else self.rows.items():
            self._rows_int2date(rows)
            ret.extend(rows)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def prepare_data(self, rows):
        """
        Sets and prepares the rows. The rows are stored in groups in a dictionary. A group is a list of rows with the
        same natural key. The key in the dictionary is a tuple with the values of the natural key.

        :param list[dict] rows: The rows
        """
        self.rows = dict()
        for row in copy.copy(rows) if self._copy else rows:
            natural_key = self._get_natural_key(row)
            if natural_key not in self.rows:
                self.rows[natural_key] = list()
            self.rows[natural_key].append(row)

        # Convert begin and end dates to integers.
        self._date_type = None
        for natural_key, rows in self.rows.items():
            self.rows[natural_key] = self._rows_date2int(rows)

# ----------------------------------------------------------------------------------------------------------------------
