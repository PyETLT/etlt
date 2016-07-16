import copy
import unittest

from etlt.helper.Type2Helper import Type2Helper


class Type2HelperTest(unittest.TestCase):
    """
    Test cases for Type2Helper
    """

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge01(self):
        """
        Test merge with Allen.X_BEFORE_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      '2',
                 'c':      3,
                 'start1': '2000-01-01',
                 'end1':   '2000-01-31',
                 'start2': '2000-03-01',
                 'end2':   '2000-03-31',
                 'value1': 10.0}]

        helper = Type2Helper('start1', 'end1', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([('start2', 'end2')])

        self.assertListEqual(rows, [])

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge02(self):
        """
        Test merge with Allen.X_MEETS_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start1': '2000-01-01',
                 'end1':   '2000-01-31',
                 'start2': '2000-02-01',
                 'end2':   '2000-02-29',
                 'value1': 10.0}]

        helper = Type2Helper('start1', 'end1', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([('start2', 'end2')])

        self.assertListEqual(rows, [])

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge03(self):
        """
        Test merge with Allen.X_OVERLAPS_WITH_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start1': '2000-01-01',
                 'end1':   '2000-01-31',
                 'start2': '2000-01-15',
                 'end2':   '2000-02-29',
                 'value1': 10.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start1': '2000-01-15',
                     'end1':   '2000-01-31',
                     'value1': 10.0}]

        helper = Type2Helper('start1', 'end1', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([('start2', 'end2')])

        self.assertListEqual(rows, expected)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge04(self):
        """
        Test merge with Allen.X_STARTS_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start1': '2000-01-01',
                 'end1':   '2000-01-31',
                 'start2': '2000-01-01',
                 'end2':   '2000-02-29',
                 'value1': 10.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start1': '2000-01-01',
                     'end1':   '2000-01-31',
                     'value1': 10.0}]

        helper = Type2Helper('start1', 'end1', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([('start2', 'end2')])

        self.assertListEqual(rows, expected)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge05(self):
        """
        Test merge with Allen.X_DURING_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start1': '2000-02-01',
                 'end1':   '2000-02-29',
                 'start2': '2000-01-01',
                 'end2':   '2000-03-31',
                 'value1': 10.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start1': '2000-02-01',
                     'end1':   '2000-02-29',
                     'value1': 10.0}]

        helper = Type2Helper('start1', 'end1', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([('start2', 'end2')])

        self.assertListEqual(rows, expected)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge06(self):
        """
        Test merge with Allen.X_FINISHES_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start1': '2000-02-01',
                 'end1':   '2000-03-31',
                 'start2': '2000-01-01',
                 'end2':   '2000-03-31',
                 'value1': 10.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start1': '2000-02-01',
                     'end1':   '2000-03-31',
                     'value1': 10.0}]

        helper = Type2Helper('start1', 'end1', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([('start2', 'end2')])

        self.assertListEqual(rows, expected)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge07(self):
        """
        Test merge with Allen.X_EQUAL_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start1': '2000-02-01',
                 'end1':   '2000-03-31',
                 'start2': '2000-02-01',
                 'end2':   '2000-03-31',
                 'value1': 10.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start1': '2000-02-01',
                     'end1':   '2000-03-31',
                     'value1': 10.0}]

        helper = Type2Helper('start1', 'end1', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([('start2', 'end2')])

        self.assertListEqual(rows, expected)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge11(self):
        """
        Test merge with Allen.X_BEFORE_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-01',
                 'end':    '2000-01-31',
                 'value1': 10.0},
                {'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-03-01',
                 'end':    '2000-03-31',
                 'value1': 10.0}]

        expected = copy.copy(rows)

        helper = Type2Helper('start', 'end', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([])

        self.assertListEqual(expected, rows)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge12(self):
        """
        Test merge with Allen.X_MEETS_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-01',
                 'end':    '2000-01-31',
                 'value1': 10.0},
                {'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-02-01',
                 'end':    '2000-02-29',
                 'value1': 10.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start':  '2000-01-01',
                     'end':    '2000-02-29',
                     'value1': 10.0}]

        helper = Type2Helper('start', 'end', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([])

        self.assertListEqual(expected, rows)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge13a(self):
        """
        Test merge with Allen.X_OVERLAPS_WITH_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-01',
                 'end':    '2000-01-31',
                 'value1': 10.0},
                {'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-15',
                 'end':    '2000-02-29',
                 'value1': 10.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start':  '2000-01-01',
                     'end':    '2000-02-29',
                     'value1': 10.0}]

        helper = Type2Helper('start', 'end', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([])

        self.assertListEqual(rows, expected)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge13b(self):
        """
        Test merge with Allen.X_OVERLAPS_WITH_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-01',
                 'end':    '2000-01-31',
                 'value1': 10.0},
                {'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-15',
                 'end':    '2000-02-29',
                 'value1': 11.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start':  '2000-01-01',
                     'end':    '2000-01-14',
                     'value1': 10.0},
                    {'a':      1,
                     'b':      2,
                     'c':      3,
                     'start':  '2000-01-15',
                     'end':    '2000-02-29',
                     'value1': 11.0}]

        helper = Type2Helper('start', 'end', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([])

        self.assertListEqual(rows, expected)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge14a(self):
        """
        Test merge with Allen.X_STARTS_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-01',
                 'end':    '2000-01-31',
                 'value1': 10.0},
                {'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-01',
                 'end':    '2000-02-29',
                 'value1': 10.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start':  '2000-01-01',
                     'end':    '2000-02-29',
                     'value1': 10.0}]

        helper = Type2Helper('start', 'end', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([])

        self.assertListEqual(rows, expected)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge14b(self):
        """
        Test merge with Allen.X_STARTS_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-01',
                 'end':    '2000-01-31',
                 'value1': 10.0},
                {'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-01',
                 'end':    '2000-02-29',
                 'value1': 11.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start':  '2000-01-01',
                     'end':    '2000-02-29',
                     'value1': 11.0}]

        helper = Type2Helper('start', 'end', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([])

        self.assertListEqual(rows, expected)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge15a(self):
        """
        Test merge with Allen.X_DURING_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-01',
                 'end':    '2000-02-29',
                 'value1': 10.0},
                {'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-01',
                 'end':    '2000-02-29',
                 'value1': 10.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start':  '2000-01-01',
                     'end':    '2000-02-29',
                     'value1': 10.0}]

        helper = Type2Helper('start', 'end', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([])

        self.assertListEqual(rows, expected)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge15b(self):
        """
        Test merge with Allen.X_DURING_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-01',
                 'end':    '2000-02-29',
                 'value1': 10.0},
                {'a':      1,
                 'b':      2,
                 'c':      3,
                 'start':  '2000-01-01',
                 'end':    '2000-02-29',
                 'value1': 11.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start':  '2000-01-01',
                     'end':    '2000-02-29',
                     'value1': 11.0}]

        helper = Type2Helper('start', 'end', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([])

        self.assertListEqual(rows, expected)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge16(self):
        """
        Test merge with Allen.X_FINISHES_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start1': '2000-02-01',
                 'end1':   '2000-03-31',
                 'start2': '2000-01-01',
                 'end2':   '2000-03-31',
                 'value1': 10.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start1': '2000-02-01',
                     'end1':   '2000-03-31',
                     'value1': 10.0}]

        helper = Type2Helper('start1', 'end1', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([('start2', 'end2')])

        self.assertListEqual(rows, expected)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge17(self):
        """
        Test merge with Allen.X_EQUAL_Y intervals.
        :return:
        """
        rows = [{'a':      1,
                 'b':      2,
                 'c':      3,
                 'start1': '2000-02-01',
                 'end1':   '2000-03-31',
                 'start2': '2000-02-01',
                 'end2':   '2000-03-31',
                 'value1': 10.0}]

        expected = [{'a':      1,
                     'b':      2,
                     'c':      3,
                     'start1': '2000-02-01',
                     'end1':   '2000-03-31',
                     'value1': 10.0}]

        helper = Type2Helper('start1', 'end1', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([('start2', 'end2')])

        self.assertListEqual(rows, expected)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge99(self):
        rows1 = [{'a': 1, 'b': 1, 'start1': '2000-01-01', 'end1': '2000-01-14', 'value1': 10.0},
                 {'a': 1, 'b': 1, 'start1': '2000-01-15', 'end1': '2000-01-31', 'value1': 10.1},
                 {'a': 1, 'b': 1, 'start1': '2000-02-01', 'end1': '2000-02-29', 'value1': 10.2},
                 {'a': 2, 'b': 3, 'start1': '2000-01-01', 'end1': '2000-01-31', 'value1': 20.0},
                 {'a': 3, 'b': 3, 'start1': '2000-02-01', 'end1': '2000-02-29', 'value1': 20.1}]

        rows2 = [{'b': 1, 'c': 4, 'start2': '2000-01-01', 'end2': '2000-01-20', 'value2': 1.0},
                 {'b': 1, 'c': 5, 'start2': '2000-01-10', 'end2': '2000-01-14', 'value2': 1.1},
                 {'b': 1, 'c': 6, 'start2': '2000-02-15', 'end2': '2000-02-29', 'value2': 1.2},
                 {'b': 3, 'c': 7, 'start2': '2000-01-01', 'end2': '2000-02-10', 'value2': 2.0},
                 {'b': 3, 'c': 8, 'start2': '2000-02-11', 'end2': '2000-02-20', 'value2': 2.1},
                 {'b': 3, 'c': 9, 'start2': '2000-02-21', 'end2': '2000-03-30', 'value2': 2.2}]

        rows = list()
        for row1 in rows1:
            for row2 in rows2:
                if row1['b'] == row2['b']:
                    tmp = copy.copy(row1)
                    tmp.update(row2)
                    rows.append(tmp)

        expected = [{'a':      1,
                     'b':      1,
                     'c':      4,
                     'end1':   '2000-01-14',
                     'start1': '2000-01-01',
                     'value1': 10.0,
                     'value2': 1.0},
                    {'a':      1,
                     'b':      1,
                     'c':      4,
                     'end1':   '2000-01-20',
                     'start1': '2000-01-15',
                     'value1': 10.1,
                     'value2': 1.0},
                    {'a':      1,
                     'b':      1,
                     'c':      5,
                     'end1':   '2000-01-14',
                     'start1': '2000-01-10',
                     'value1': 10.0,
                     'value2': 1.1},
                    {'a':      1,
                     'b':      1,
                     'c':      6,
                     'end1':   '2000-02-29',
                     'start1': '2000-02-15',
                     'value1': 10.2,
                     'value2': 1.2},
                    {'a':      2,
                     'b':      3,
                     'c':      7,
                     'end1':   '2000-01-31',
                     'start1': '2000-01-01',
                     'value1': 20.0,
                     'value2': 2.0},
                    {'a':      3,
                     'b':      3,
                     'c':      7,
                     'end1':   '2000-02-10',
                     'start1': '2000-02-01',
                     'value1': 20.1,
                     'value2': 2.0},
                    {'a':      3,
                     'b':      3,
                     'c':      8,
                     'end1':   '2000-02-20',
                     'start1': '2000-02-11',
                     'value1': 20.1,
                     'value2': 2.1},
                    {'a':      3,
                     'b':      3,
                     'c':      9,
                     'end1':   '2000-02-29',
                     'start1': '2000-02-21',
                     'value1': 20.1,
                     'value2': 2.2}]

        helper = Type2Helper('start1', 'end1', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        rows = helper.merge([('start2', 'end2')])
        rows = sorted(rows, key=lambda row: (row['a'], row['b'], row['c'], row['start1']))

        self.assertListEqual(rows, expected)

# ----------------------------------------------------------------------------------------------------------------------
