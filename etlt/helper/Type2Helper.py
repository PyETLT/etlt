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

        :type list[str]:
        """

        self._key_end_date = key_end_date
        """
        The key of the end date in the rows.

        :type str:
        """
        self._key_start_date = key_start_date
        """
        The key of the start date in the rows.

        :type str:
        """

        self.rows = dict()
        """
        The data set.

        :type dict:
        """

        self._date_type = ''
        """
        The type of the date fields.
        - date for datetime.date objects
        - str  for strings in ISO 8601 (YYYY-MM-DD) format.

        :type str:
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
            tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
            return tmp.toordinal()

        if isinstance(date, datetime.date):
            return date.toordinal()

        raise ValueError('Unexpected type %s' % date.__class__)

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

        raise ValueError('Unexpected type %s' % date.__class__)

    # ------------------------------------------------------------------------------------------------------------------
    def _sort_data(self):
        """
        Sorts all rows in all groups by start and end date.
        """
        for natural_key, rows in self.rows.items():
            self.rows[natural_key] = sorted(rows, key=lambda row: (row[self._key_start_date], row[self._key_end_date]))

    # ------------------------------------------------------------------------------------------------------------------
    def prepare_data(self, rows):
        """
        Sets and prepares the rows. The rows are stored in groups in a dictionary. A group is a list of rows with the
        same natural key. The key in the dictionary is a tuple with the values of the natural key.

        :param list[dict] rows: The rows
        """
        self.rows = dict()
        for row in rows:
            natural_key = self._get_natural_key(row)
            if natural_key not in self.rows:
                self.rows[natural_key] = list()
            self.rows[natural_key].append(row)

    # ------------------------------------------------------------------------------------------------------------------
    def detect_overlap(self):
        """
        Detects if two or more rows in a group (i.e. rows with the same natural key) have overlap. Returns the rows with
        overlap.
        """
        ret = dict()
        for (natural_key, rows) in self.rows:
            prev_row = None
            added_prev_row = False
            overlapping = list()
            for row in rows:
                if prev_row:
                    relation = Allen.relation(self._date2int(row[self._key_start_date]),
                                              self._date2int(row[self._key_end_date]),
                                              self._date2int(prev_row[self._key_start_date]),
                                              self._date2int(prev_row[self._key_end_date]))
                    if relation not in [Allen.X_BEFORE_Y, Allen.X_MEETS_Y]:
                        if not added_prev_row:
                            overlapping.append(prev_row)
                        overlapping.append(row)
                        added_prev_row = True
                    else:
                        added_prev_row = False

                    prev_row = row

            if overlapping:
                ret[natural_key] = overlapping

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _intersect(start1, end1, start2, end2):
        """
        Returns the intersection of two intervals. Returns (None,None) if the intersection is empty.

        :param str|datetime.date start1: The start date of the first interval.
        :param str|datetime.date end1: The end date of the first interval.
        :param str|datetime.date start2: The start date of the second interval.
        :param str|datetime.date end2: The end date of the second interval.

        :rtype: tuple[datetime.date|None,datetime.date|None]
        """
        start = max(start1, start2)
        end = min(end1, end2)

        if start > end:
            return None, None

        return start, end

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
    def _merge_pass1(self, keys, rows):
        """
        Replaces start and end dates in the row set with their integer representation

        :param list[tuple[str,str]] keys: The other keys with start and end date.
        :param list[dict[str,T]] rows: The list of rows.

        :rtype: list[dict[str,T]]
        """
        ret = list()
        for row in rows:
            # Make a copy of the row such that self._rows is not affected by merge.
            tmp = copy.copy(row)

            # Determine the type of dates based on the first start date.
            if not self._date_type:
                self._date_type = self._get_date_type(tmp[self._key_start_date])

            # Convert dates to integers.
            tmp[self._key_start_date] = self._date2int(tmp[self._key_start_date])
            tmp[self._key_end_date] = self._date2int(tmp[self._key_end_date])
            for key_start_date, key_end_date in keys:
                if key_start_date != self._key_start_date:
                    tmp[key_start_date] = self._date2int(tmp[key_start_date])
                if key_end_date != self._key_end_date:
                    tmp[key_end_date] = self._date2int(tmp[key_end_date])
            ret.append(tmp)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def _merge_pass2(self, keys, rows):
        """
        Computes the intersection of the date intervals of two or more reference data sets. If the intersection is empty
        the row is removed from the group.

        :param list[tuple[str,str]] keys: The other keys with start and end date.
        :param list[dict[str,T]] rows: The list of rows.

        :rtype: list[dict[str,T]]
        """
        ret = list()
        for row in rows:
            start_date = row[self._key_start_date]
            end_date = row[self._key_end_date]
            for key_start_date, key_end_date in keys:
                start_date, end_date = Type2Helper._intersect(start_date,
                                                              end_date,
                                                              row[key_start_date],
                                                              row[key_end_date])
                if not start_date:
                    break
                if self._key_start_date != key_start_date:
                    del row[key_start_date]
                if self._key_end_date != key_end_date:
                    del row[key_end_date]

            if start_date:
                row[self._key_start_date] = start_date
                row[self._key_end_date] = end_date
                ret.append(row)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def _merge_pass3(self, rows):
        """
        Returns a list of rows sorted by start and end date.

        :param list[dict[str,T]] rows: The list of rows.

        :rtype: list[dict[str,T]]
        """
        return sorted(rows, key=lambda row: (row[self._key_start_date], row[self._key_end_date]))

    # ------------------------------------------------------------------------------------------------------------------
    def _merge_pass4(self, rows):
        """
        Merges adjacent and overlapping rows in the same group (i.e. with the same natural key).

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
                if relation == Allen.X_BEFORE_Y:
                    # Two rows with distinct intervals.
                    ret.append(prev_row)
                    prev_row = row
                elif relation == Allen.X_MEETS_Y:
                    # The two rows are adjacent.
                    if self._equal(prev_row, row):
                        # The two rows are identical (except for start and end date) and adjacent. Combine the two rows
                        # into one row.
                        prev_row[self._key_end_date] = row[self._key_end_date]
                    else:
                        # Rows are adjacent but not identical.
                        ret.append(prev_row)
                        prev_row = row
                elif relation == Allen.X_OVERLAPS_WITH_Y:
                    # Should not occur with proper reference data.
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
                    # Should not occur with proper reference data.
                    prev_row = row
                elif relation == Allen.X_EQUAL_Y:
                    # Can happen when the reference data sets are joined without respect for date intervals.
                    prev_row = row
                else:
                    raise ValueError('Data is not sorted properly')
            else:
                prev_row = row

        if prev_row:
            ret.append(prev_row)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def _merge_pass5(self, rows):
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
            else:
                raise ValueError('Unexpected date type %s' % self._date_type)

    # ------------------------------------------------------------------------------------------------------------------
    def merge(self, keys):
        """
        Merges the join on natural keys of two or more reference data sets.

        :param list[tuple[str,str]] keys: For each data set the keys of the start and end date.

        :rtype: list[dict[str,T]]
        """
        ret = list()
        self._date_type = ''
        for rows in self.rows.values():
            tmp = self._merge_pass1(keys, rows)
            tmp = self._merge_pass2(keys, tmp)
            if tmp:
                tmp = self._merge_pass3(tmp)
                tmp = self._merge_pass4(tmp)
                self._merge_pass5(tmp)

            ret.extend(tmp)

        return ret

# ----------------------------------------------------------------------------------------------------------------------
