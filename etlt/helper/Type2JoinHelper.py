"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import copy

from etlt.helper.Allen import Allen
from etlt.helper.Type2Helper import Type2Helper


class Type2JoinHelper(Type2Helper):
    """
    A helper class for joining data sets with date intervals.
    """

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
    @staticmethod
    def _intersect(start1, end1, start2, end2):
        """
        Returns the intersection of two intervals. Returns (None,None) if the intersection is empty.

        :param int start1: The start date of the first interval.
        :param int end1: The end date of the first interval.
        :param int start2: The start date of the second interval.
        :param int end2: The end date of the second interval.

        :rtype: tuple[int|None,int|None]
        """
        start = max(start1, start2)
        end = min(end1, end2)

        if start > end:
            return None, None

        return start, end

    # ------------------------------------------------------------------------------------------------------------------
    def _pass1(self, keys, rows):
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
    def _pass2(self, keys, rows):
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
                start_date, end_date = Type2JoinHelper._intersect(start_date,
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
    def _pass3(self, rows):
        """
        Returns a list of rows sorted by start and end date.

        :param list[dict[str,T]] rows: The list of rows.

        :rtype: list[dict[str,T]]
        """
        return sorted(rows, key=lambda row: (row[self._key_start_date], row[self._key_end_date]))

    # ------------------------------------------------------------------------------------------------------------------
    def _pass4(self, rows):
        """
        Merges adjacent and overlapping rows in the same group (i.e. with the same natural key). With proper reference
        data overlapping rows MUST not occur. However, this  method can handle overlapping rows. Overlapping rows are
        resolved as follows:
        * The interval with the most recent begin date prevails for the overlapping period.
        * If the begin dates are the same the interval with the most recent end date prevails.
        * If the begin and end dates are equal the last row in the data set prevails.

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
                    if not self._equal(prev_row, row):
                        prev_row[self._key_end_date] = row[self._key_start_date] - 1
                        ret.append(prev_row)
                        prev_row = row
                        # Note: the interval after row[self._key_end_date] is discarded.

                    # Note: if the two rows are identical (except for start and end date) nothing to do.
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
                    # Not in _pass3 the rows are sorted such that.
                    # prev_row[self._key_begin_date] <= row[self._key_begin_date]. Hence the following relation should
                    # not occur: X_FINISHES_Y, X_BEFORE_Y_INVERSE, X_MEETS_Y_INVERSE, X_OVERLAPS_WITH_Y_INVERSE, and
                    # X_STARTS_Y_INVERSE. Hence, we covered all 13 relations in Allen's interval algebra.
                    raise ValueError('Data is not sorted properly. Relation: %d' % relation)
            else:
                prev_row = row

        if prev_row:
            ret.append(prev_row)

        return ret

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
            tmp = self._pass1(keys, rows)
            tmp = self._pass2(keys, tmp)
            if tmp:
                tmp = self._pass3(tmp)
                tmp = self._pass4(tmp)
                self._rows_int2date(tmp)

            ret.extend(tmp)

        return ret

# ----------------------------------------------------------------------------------------------------------------------
