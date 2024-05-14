import unittest
from typing import Optional, Tuple

from etlt.helper.Allen import Allen


class AllenTest(unittest.TestCase):
    """
    Test cases for class Allen algebra.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _test1(self, expected: Optional[int], x: Tuple[int, int], y: Tuple[int, int]) -> None:
        relation1 = Allen.relation(x[0], x[1], y[0], y[1])
        self.assertEqual(expected, relation1)

        relation2 = Allen.relation(y[0], y[1], x[0], x[1])
        self.assertEqual(relation1, -1 * relation2)

        relation3 = Allen.relation(x[1], x[0], y[0], y[1])
        self.assertIsNone(relation3)

        relation4 = Allen.relation(x[0], x[1], y[1], y[0])
        self.assertIsNone(relation4)

        relation5 = Allen.relation(x[1], x[0], y[1], y[0])
        self.assertIsNone(relation5)

        relation6 = Allen.relation(y[1], y[0], x[0], x[1])
        self.assertIsNone(relation6)

        relation7 = Allen.relation(y[0], y[1], x[1], x[0])
        self.assertIsNone(relation7)

        relation8 = Allen.relation(y[1], y[0], x[1], x[0])
        self.assertIsNone(relation8)

    # ------------------------------------------------------------------------------------------------------------------
    def test_x_takes_place_before_y(self) -> None:
        self._test1(Allen.X_BEFORE_Y, (1, 3), (5, 7))

    # ------------------------------------------------------------------------------------------------------------------
    def test_x_meets_y(self) -> None:
        self._test1(Allen.X_MEETS_Y, (1, 2), (3, 5))

    # ------------------------------------------------------------------------------------------------------------------
    def test_x_overlaps_with_y(self) -> None:
        self._test1(Allen.X_OVERLAPS_WITH_Y, (1, 4), (3, 5))
        self._test1(Allen.X_OVERLAPS_WITH_Y, (1, 3), (3, 5))

    # ------------------------------------------------------------------------------------------------------------------
    def test_x_starts_y(self) -> None:
        self._test1(Allen.X_STARTS_Y, (1, 2), (1, 5))

    # ------------------------------------------------------------------------------------------------------------------
    def test_x_during_y(self) -> None:
        self._test1(Allen.X_DURING_Y, (2, 3), (1, 5))

    # ------------------------------------------------------------------------------------------------------------------
    def test_x_finish_y(self) -> None:
        self._test1(Allen.X_FINISHES_Y, (3, 5), (1, 5))

    # ------------------------------------------------------------------------------------------------------------------
    def test_x_equal_y(self) -> None:
        self._test1(Allen.X_EQUAL_Y, (1, 5), (1, 5))

# ----------------------------------------------------------------------------------------------------------------------
