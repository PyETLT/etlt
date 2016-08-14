"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""


class Allen:
    """
    Utility class for Allen's interval algebra, https://en.wikipedia.org/wiki/Allen%27s_interval_algebra.
    """
    # ------------------------------------------------------------------------------------------------------------------
    X_BEFORE_Y = 1
    X_MEETS_Y = 2
    X_OVERLAPS_WITH_Y = 3
    X_STARTS_Y = 4
    X_DURING_Y = 5
    X_FINISHES_Y = 6
    X_EQUAL_Y = 0
    X_BEFORE_Y_INVERSE = -1
    X_MEETS_Y_INVERSE = -2
    X_OVERLAPS_WITH_Y_INVERSE = -3
    X_STARTS_Y_INVERSE = -4
    X_DURING_Y_INVERSE = -5
    X_FINISHES_Y_INVERSE = -6

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def relation(x_start, x_end, y_start, y_end):
        """
        Returns the relation between two intervals.

        :param int x_start: The start point of the first interval.
        :param int x_end: The end point of the first interval.
        :param int y_start: The start point of the second interval.
        :param int y_end: The end point of the second interval.

        :rtype: int|None
        """

        if (x_end - x_start) < 0 or (y_end - y_start) < 0:
            return None

        diff_end = y_end - x_end

        if diff_end < 0:
            return -Allen.relation(y_start, y_end, x_start, x_end)

        diff_start = y_start - x_start
        gab = y_start - x_end

        if diff_end == 0:
            if diff_start == 0:
                return Allen.X_EQUAL_Y

            if diff_start < 0:
                return Allen.X_FINISHES_Y

            return Allen.X_FINISHES_Y_INVERSE

        if gab > 1:
            return Allen.X_BEFORE_Y

        if gab == 1:
            return Allen.X_MEETS_Y

        if diff_start > 0:
            return Allen.X_OVERLAPS_WITH_Y

        if diff_start == 0:
            return Allen.X_STARTS_Y

        if diff_start < 0:
            return Allen.X_DURING_Y

# ----------------------------------------------------------------------------------------------------------------------
