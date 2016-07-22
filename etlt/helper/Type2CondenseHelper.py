"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import copy

from etlt.helper.Allen import Allen
from etlt.helper.Type2Helper import Type2Helper


class Type2CondenseHelper(Type2Helper):
    """
    A helper class for deriving the distinct intervals in reference data with date intervals.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _distinct(start1, end1, start2, end2):
        """
        Returns a list of distinct (or none overlapping) intervals if two intervals are not distinct. Returns None if
        the two intervals are distinct. The list can have 2 or 3 intervals.

        :param int start1: The start date of the first interval.
        :param int end1: The end date of the first interval.
        :param int start2: The start date of the second interval.
        :param int end2: The end date of the second interval.

        :rtype: None|tuple[datetime.date|None,datetime.date|None]
        """
        relation = Allen.relation(start1, end1, start2, end2)
        if relation in [Allen.X_BEFORE_Y, Allen.X_MEETS_Y]:
            return None  # [(start1, end1), (start2, end2)]

        if relation in [Allen.X_BEFORE_Y_INVERSE, Allen.X_MEETS_Y_INVERSE]:
            return None  # [(start2, end2), (start1, end1)]

        if relation == Allen.X_OVERLAPS_WITH_Y:
            return [(start1, start2 - 1), (start2, end1), (end1 + 1, end2)]

        if relation == Allen.X_OVERLAPS_WITH_Y_INVERSE:
            return [(start2, start1 - 1), (start1, end2), (end2 + 1, end1)]

        if relation == Allen.X_STARTS_Y:
            return [(start1, end1), (end1 + 1, end2)]

        if relation == Allen.X_STARTS_Y_INVERSE:
            return [(start2, end2), (end2 + 1, end1)]

        if relation == Allen.X_DURING_Y:
            return [(start2, start1 - 1), (start1, end1), (end1 + 1, end2)]

        if relation == Allen.X_DURING_Y_INVERSE:
            return [(start1, start2 - 1), (start2, end2), (end2 + 1, end1)]

        if relation == Allen.X_FINISHES_Y:
            return [(start2, start1 - 1), (start1, end1)]

        if relation == Allen.X_FINISHES_Y_INVERSE:
            return [(start1, start2 - 1), (start2, end2)]

        if relation == Allen.X_EQUAL_Y:
            return None  # [(start1, end1)]

        raise ValueError('Unexpected relation %d' % relation)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _add(all_intervals, new_interval):
        """
        Adds a new interval to a set of distinct intervals.

        :param set[(int,int)] all_intervals: The set of distinct intervals.
        :param (int,int) new_interval: The new interval.
        """
        intervals = None
        old_interval = None
        for old_interval in all_intervals:
            intervals = Type2CondenseHelper._distinct(new_interval[0],
                                                      new_interval[1],
                                                      old_interval[0],
                                                      old_interval[1])
            if intervals:
                break

        if intervals:
            if old_interval:
                all_intervals.remove(old_interval)
            for distinct_interval in intervals:
                Type2CondenseHelper._add(all_intervals, distinct_interval)
        else:
            all_intervals.add(new_interval)

    # ------------------------------------------------------------------------------------------------------------------
    def _derive_distinct_intervals(self, rows):
        """
        Returns the set of distinct intervals in a row set.

        :param list[dict[str,T]] rows: The rows set.

        :rtype: set[(int,int)]
        """
        ret = set()
        for row in rows:
            self._add(ret, (row[self._key_start_date], row[self._key_end_date]))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def condense(self):
        """
        Returns the data set condensed to the distinct intervals based on the natural key.

        :rtype: list[dict[str,T]]
        """
        ret = list()
        self._date_type = ''
        for rows in self.rows.values():
            tmp1 = self._rows_date2int(rows)
            tmp2 = self._derive_distinct_intervals(tmp1)
            tmp2 = sorted(tmp2)
            for tmp3 in tmp2:
                tmp4 = copy.copy(rows[0])
                tmp4[self._key_start_date] = tmp3[0]
                tmp4[self._key_end_date] = tmp3[1]
                ret.append(tmp4)

        self._rows_int2date(ret)

        return ret

# ----------------------------------------------------------------------------------------------------------------------
