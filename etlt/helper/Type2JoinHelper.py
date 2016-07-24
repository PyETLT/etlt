"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
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
    def _additional_rows_date2int(self, keys, rows):
        """
        Replaces start and end dates of the additional date intervals in the row set with their integer representation

        :param list[tuple[str,str]] keys: The other keys with start and end date.
        :param list[dict[str,T]] rows: The list of rows.

        :rtype: list[dict[str,T]]
        """
        for row in rows:
            for key_start_date, key_end_date in keys:
                if key_start_date not in [self._key_start_date, self._key_end_date]:
                    row[key_start_date] = self._date2int(row[key_start_date])
                if key_end_date not in [self._key_start_date, self._key_end_date]:
                    row[key_end_date] = self._date2int(row[key_end_date])

    # ------------------------------------------------------------------------------------------------------------------
    def _intersection(self, keys, rows):
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
                if key_start_date not in [self._key_start_date, self._key_end_date]:
                    del row[key_start_date]
                if key_end_date not in [self._key_start_date, self._key_end_date]:
                    del row[key_end_date]

            if start_date:
                row[self._key_start_date] = start_date
                row[self._key_end_date] = end_date
                ret.append(row)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def _merge_adjacent_rows(self, rows):
        """
        Resolves adjacent and overlapping rows. With proper reference data overlapping rows MUST not occur. However,
        this  method can handle overlapping rows. Overlapping rows are resolved as follows:
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
                    raise ValueError('Data is not sorted properly. Relation: {0:d}'.format(relation))
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
        """
        deletes = []
        for natural_key, rows in self.rows.items():
            self._additional_rows_date2int(keys, rows)
            rows = self._intersection(keys, rows)
            if rows:
                rows = self._rows_sort(rows)
                self.rows[natural_key] = self._merge_adjacent_rows(rows)
            else:
                deletes.append(natural_key)

        for natural_key in deletes:
            del self.rows[natural_key]

# ----------------------------------------------------------------------------------------------------------------------
