from typing import Any, Dict, List, Optional, Set, Tuple

from etlt.helper.Allen import Allen
from etlt.helper.Type2Helper import Type2Helper


class Type2CondenseHelper(Type2Helper):
    """
    A helper class for deriving the distinct intervals in reference data with date intervals.

    A typical use case for this class is aggregate the reference data for a type 2 dimension into the reference data
    for another type 2 dimension at a higher in the dimension hierarchy.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _distinct(row1: Tuple[int, int], row2: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Returns a list of distinct (or none overlapping) intervals if two intervals are overlapping. Returns None if
        the two intervals are none overlapping. The list can have 2 or 3 intervals.

        :param row1: The first interval.
        :param row2: The second interval.
        """
        relation = Allen.relation(row1[0], row1[1], row2[0], row2[1])

        if relation is None:
            # One of the 2 intervals is invalid.
            return []

        if relation == Allen.X_BEFORE_Y:
            # row1: |----|
            # row2:            |-----|
            return None  # [(row1[0], row1[1]), (row2[0], row2[1])]

        if relation == Allen.X_BEFORE_Y_INVERSE:
            # row1:            |-----|
            # row2: |----|
            return None  # [(row2[0], row2[1]), (row1[0], row1[1])]

        if relation == Allen.X_MEETS_Y:
            # row1: |-------|
            # row2:          |-------|
            return None  # [(row1[0], row1[1]), (row2[0], row2[1])]

        if relation == Allen.X_MEETS_Y_INVERSE:
            # row1:          |-------|
            # row2: |-------|
            return None  # [(row2[0], row2[1]), (row1[0], row1[1])]

        if relation == Allen.X_OVERLAPS_WITH_Y:
            # row1: |-----------|
            # row2:       |----------|
            return [(row1[0], row2[0] - 1), (row2[0], row1[1]), (row1[1] + 1, row2[1])]

        if relation == Allen.X_OVERLAPS_WITH_Y_INVERSE:
            # row1:       |----------|
            # row2: |-----------|
            return [(row2[0], row1[0] - 1), (row1[0], row2[1]), (row2[1] + 1, row1[1])]

        if relation == Allen.X_STARTS_Y:
            # row1: |------|
            # row2: |----------------|
            return [(row1[0], row1[1]), (row1[1] + 1, row2[1])]

        if relation == Allen.X_STARTS_Y_INVERSE:
            # row1: |----------------|
            # row2: |------|
            return [(row2[0], row2[1]), (row2[1] + 1, row1[1])]

        if relation == Allen.X_DURING_Y:
            # row1:      |------|
            # row2: |----------------|
            return [(row2[0], row1[0] - 1), (row1[0], row1[1]), (row1[1] + 1, row2[1])]

        if relation == Allen.X_DURING_Y_INVERSE:
            # row1: |----------------|
            # row2:      |------|
            return [(row1[0], row2[0] - 1), (row2[0], row2[1]), (row2[1] + 1, row1[1])]

        if relation == Allen.X_FINISHES_Y:
            # row1:           |------|
            # row2: |----------------|
            return [(row2[0], row1[0] - 1), (row1[0], row1[1])]

        if relation == Allen.X_FINISHES_Y_INVERSE:
            # row1: |----------------|
            # row2:           |------|
            return [(row1[0], row2[0] - 1), (row2[0], row2[1])]

        if relation == Allen.X_EQUAL_Y:
            # row1: |----------------|
            # row2: |----------------|
            return None  # [(row1[0], row1[1])]

        # We got all 13 relation in Allen's interval algebra covered.
        raise ValueError('Unexpected relation {0}'.format(relation))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _add_interval(all_intervals: Set[Tuple[int, int]], new_interval: Tuple[int, int]) -> None:
        """
        Adds a new interval to a set of none overlapping intervals.

        :param all_intervals: The set of distinct intervals.
        :param new_interval: The new interval.
        """
        intervals = None
        old_interval = None
        for old_interval in all_intervals:
            intervals = Type2CondenseHelper._distinct(new_interval, old_interval)
            if intervals:
                break

        if intervals is None:
            all_intervals.add(new_interval)
        else:
            if old_interval:
                all_intervals.remove(old_interval)
            for distinct_interval in intervals:
                Type2CondenseHelper._add_interval(all_intervals, distinct_interval)

    # ------------------------------------------------------------------------------------------------------------------
    def _derive_distinct_intervals(self, rows: List[Dict[str, Any]]) -> Set[Tuple[int, int]]:
        """
        Returns the set of distinct intervals in a row set.

        :param rows: The rows set.
        """
        ret = set()
        for row in rows:
            self._add_interval(ret, (row[self._key_start_date], row[self._key_end_date]))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def condense(self) -> None:
        """
        Condense the data set to the distinct intervals based on the pseudo key.
        """
        for pseudo_key, rows in self._rows.items():
            tmp1 = []
            intervals = sorted(self._derive_distinct_intervals(rows))
            for interval in intervals:
                tmp2 = dict(zip(self._pseudo_key, pseudo_key))
                tmp2[self._key_start_date] = interval[0]
                tmp2[self._key_end_date] = interval[1]
                tmp1.append(tmp2)

            self._rows[pseudo_key] = tmp1

# ----------------------------------------------------------------------------------------------------------------------
