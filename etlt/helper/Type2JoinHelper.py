"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
from etlt.helper.Type2Helper import Type2Helper


class Type2JoinHelper(Type2Helper):
    """
    A helper class for joining data sets with date intervals.
    """

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
        # If there are no other keys with start and end date (i.e. nothing to merge) return immediately.
        if not keys:
            return rows

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
    def merge(self, keys):
        """
        Merges the join on pseudo keys of two or more reference data sets.

        :param list[tuple[str,str]] keys: For each data set the keys of the start and end date.
        """
        deletes = []
        for pseudo_key, rows in self._rows.items():
            self._additional_rows_date2int(keys, rows)
            rows = self._intersection(keys, rows)
            if rows:
                rows = self._rows_sort(rows)
                self._rows[pseudo_key] = self._merge_adjacent_rows(rows)
            else:
                deletes.append(pseudo_key)

        for pseudo_key in deletes:
            del self._rows[pseudo_key]

# ----------------------------------------------------------------------------------------------------------------------
