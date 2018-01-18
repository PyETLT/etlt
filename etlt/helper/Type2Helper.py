"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import copy
import datetime

from etlt.helper.Allen import Allen


class Type2Helper:
    """
    A helper class for reference data with date intervals.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, key_start_date, key_end_date, pseudo_key):
        """
        Object constructor.

        :param str key_start_date: The key of the start date in the rows.
        :param str key_end_date: The key of the end date in the rows.
        :param list[str] pseudo_key: The keys of the columns that form the pseudo key.
        """
        self.copy = True
        """
        If set to true a copy will be made from the original rows such that the original rows are not modified.

         :type: bool
        """

        self._pseudo_key = list(pseudo_key)
        """
        The keys of the columns that form the pseudo key.

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

        self._rows = dict()
        """
        The data set.

        :type: dict
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
    def _get_pseudo_key(self, row):
        """
        Returns the pseudo key in a row.

        :param dict row: The row.

        :rtype: tuple
        """
        ret = list()
        for key in self._pseudo_key:
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
        """
        for row in rows:
            # Determine the type of dates based on the first start date.
            if not self._date_type:
                self._date_type = self._get_date_type(row[self._key_start_date])

            # Convert dates to integers.
            row[self._key_start_date] = self._date2int(row[self._key_start_date])
            row[self._key_end_date] = self._date2int(row[self._key_end_date])

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
    def _equal(self, row1, row2):
        """
        Returns True if two rows are identical excluding start and end date. Returns False otherwise.

        :param dict[str,T] row1: The first row.
        :param dict[str,T] row2: The second row.

        :rtype: bool
        """
        for key in row1.keys():
            if key not in [self._key_start_date, self._key_end_date]:
                if row1[key] != row2[key]:
                    return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    def _merge_adjacent_rows(self, rows):
        """
        Resolves adjacent and overlapping rows. Overlapping rows are resolved as follows:
        * The interval with the most recent begin date prevails for the overlapping period.
        * If the begin dates are the same the interval with the most recent end date prevails.
        * If the begin and end dates are equal the last row in the data set prevails.
        Identical (excluding begin and end date) adjacent rows are replace with a single row.

        :param list[dict[str,T]] rows: The rows in a group (i.e. with the same natural key).
        .
        :rtype: list[dict[str,T]]
        """
        ret = list()

        prev_row = None
        for row in rows:
            if prev_row:
                relation = Allen.relation(prev_row[self._key_start_date],
                                          prev_row[self._key_end_date],
                                          row[self._key_start_date],
                                          row[self._key_end_date])
                if relation is None:
                    # row holds an invalid interval (prev_row always holds a valid interval). Hence, the join is empty.
                    return []

                elif relation == Allen.X_BEFORE_Y:
                    # Two rows with distinct intervals.
                    # prev_row: |----|
                    # row:                 |-----|
                    ret.append(prev_row)
                    prev_row = row

                elif relation == Allen.X_MEETS_Y:
                    # The two rows are adjacent.
                    # prev_row: |-------|
                    # row:               |-------|
                    if self._equal(prev_row, row):
                        # The two rows are identical (except for start and end date) and adjacent. Combine the two rows
                        # into one row.
                        prev_row[self._key_end_date] = row[self._key_end_date]
                    else:
                        # Rows are adjacent but not identical.
                        ret.append(prev_row)
                        prev_row = row

                elif relation == Allen.X_OVERLAPS_WITH_Y:
                    # prev_row overlaps row. Should not occur with proper reference data.
                    # prev_row: |-----------|
                    # row:            |----------|
                    if self._equal(prev_row, row):
                        # The two rows are identical (except for start and end date) and overlapping. Combine the two
                        # rows into one row.
                        prev_row[self._key_end_date] = row[self._key_end_date]
                    else:
                        # Rows are overlapping but not identical.
                        prev_row[self._key_end_date] = row[self._key_start_date] - 1
                        ret.append(prev_row)
                        prev_row = row

                elif relation == Allen.X_STARTS_Y:
                    # prev_row start row. Should not occur with proper reference data.
                    # prev_row: |------|
                    # row:      |----------------|
                    prev_row = row

                elif relation == Allen.X_EQUAL_Y:
                    # Can happen when the reference data sets are joined without respect for date intervals.
                    # prev_row: |----------------|
                    # row:      |----------------|
                    prev_row = row

                elif relation == Allen.X_DURING_Y_INVERSE:
                    # row during prev_row. Should not occur with proper reference data.
                    # prev_row: |----------------|
                    # row:           |------|
                    # Note: the interval with the most recent start date prevails. Hence, the interval after
                    # row[self._key_end_date] is discarded.
                    if self._equal(prev_row, row):
                        prev_row[self._key_end_date] = row[self._key_end_date]
                    else:
                        prev_row[self._key_end_date] = row[self._key_start_date] - 1
                        ret.append(prev_row)
                        prev_row = row

                elif relation == Allen.X_FINISHES_Y_INVERSE:
                    # row finishes prev_row. Should not occur with proper reference data.
                    # prev_row: |----------------|
                    # row:                |------|
                    if not self._equal(prev_row, row):
                        prev_row[self._key_end_date] = row[self._key_start_date] - 1
                        ret.append(prev_row)
                        prev_row = row

                        # Note: if the two rows are identical (except for start and end date) nothing to do.
                else:
                    # Note: The rows are sorted such that prev_row[self._key_begin_date] <= row[self._key_begin_date].
                    # Hence the following relation should not occur: X_DURING_Y,  X_FINISHES_Y, X_BEFORE_Y_INVERSE,
                    # X_MEETS_Y_INVERSE, X_OVERLAPS_WITH_Y_INVERSE, and X_STARTS_Y_INVERSE. Hence, we covered all 13
                    # relations in Allen's interval algebra.
                    raise ValueError('Data is not sorted properly. Relation: {0}'.format(relation))

            elif row[self._key_start_date] <= row[self._key_end_date]:
                # row is the first valid row.
                prev_row = row

        if prev_row:
            ret.append(prev_row)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def enumerate(self, name, start=1):
        """
        Enumerates all rows such that the pseudo key and the ordinal number are a unique key.

        :param str name: The key holding the ordinal number.
        :param int start: The start of the ordinal numbers. Foreach pseudo key the first row has this ordinal number.
        """
        for pseudo_key, rows in self._rows.items():
            rows = self._rows_sort(rows)
            ordinal = start
            for row in rows:
                row[name] = ordinal
                ordinal += 1
            self._rows[pseudo_key] = rows

    # ------------------------------------------------------------------------------------------------------------------
    def get_rows(self, sort=False):
        """
        Returns the rows of this Type2Helper.

        :param bool sort: If True the rows are sorted by the pseudo key.
        """
        ret = []
        for _, rows in sorted(self._rows.items()) if sort else self._rows.items():
            self._rows_int2date(rows)
            ret.extend(rows)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def prepare_data(self, rows):
        """
        Sets and prepares the rows. The rows are stored in groups in a dictionary. A group is a list of rows with the
        same pseudo key. The key in the dictionary is a tuple with the values of the pseudo key.

        :param list[dict] rows: The rows
        """
        self._rows = dict()
        for row in copy.copy(rows) if self.copy else rows:
            pseudo_key = self._get_pseudo_key(row)
            if pseudo_key not in self._rows:
                self._rows[pseudo_key] = list()
            self._rows[pseudo_key].append(row)

        # Convert begin and end dates to integers.
        self._date_type = None
        for pseudo_key, rows in self._rows.items():
            self._rows_date2int(rows)

# ----------------------------------------------------------------------------------------------------------------------
