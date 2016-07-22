import unittest

from etlt.helper.Type2CondenseHelper import Type2CondenseHelper


class Type2CondenseHelperTest(unittest.TestCase):
    """
    Test cases for Type2CondenseHelperTest
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _drop_field(rows, field):
        for row in rows:
            del row[field]

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge01a(self):
        """
        Test condense with 1 interval and one row.
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-12-31'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-12-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge01b(self):
        """
        Test condense with 1 interval and 2 rows (X is equal to Y).
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-12-31'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-01-01',
                 'end':    '2010-12-31'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-12-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge02a(self):
        """
        Test condense with 2 distinct intervals and 2 rows (X takes place before Y).
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-01-31'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-02-01',
                 'end':    '2010-02-28'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-01-31'},
                    {'year':  '2010',
                     'start': '2010-02-01',
                     'end':   '2010-02-28'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge02b(self):
        """
        Test condense with 2 distinct intervals and 2 rows.
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-01-31'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-02-01',
                 'end':    '2010-02-28'},
                {'year':   '2010',
                 'period': '3',
                 'start':  '2010-02-01',
                 'end':    '2010-02-28'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-01-31'},
                    {'year':  '2010',
                     'start': '2010-02-01',
                     'end':   '2010-02-28'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge02c(self):
        """
        Test condense with 2 distinct intervals and 2 rows (X takes place before Y).
        """
        rows = [{'year':   '2010',
                 'period': '2',
                 'start':  '2010-02-01',
                 'end':    '2010-02-28'},
                {'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-01-31'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-01-31'},
                    {'year':  '2010',
                     'start': '2010-02-01',
                     'end':   '2010-02-28'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge03a(self):
        """
        Test condense with 2 overlapping intervals and 2 rows (X overlaps with Y).
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-02-28'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-02-01',
                 'end':    '2010-03-31'}
                ]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-01-31'},
                    {'year':  '2010',
                     'start': '2010-02-01',
                     'end':   '2010-02-28'},
                    {'year':  '2010',
                     'start': '2010-03-01',
                     'end':   '2010-03-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge03b(self):
        """
        Test condense with 2 overlapping intervals and 3 rows.
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-02-28'},
                {'year':   '2010',
                 'period': '3',
                 'start':  '2010-01-01',
                 'end':    '2010-02-28'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-02-01',
                 'end':    '2010-03-31'}
                ]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-01-31'},
                    {'year':  '2010',
                     'start': '2010-02-01',
                     'end':   '2010-02-28'},
                    {'year':  '2010',
                     'start': '2010-03-01',
                     'end':   '2010-03-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge03c(self):
        """
        Test condense with 2 overlapping intervals and 2 rows (X overlaps with Y).
        """
        rows = [{'year':   '2010',
                 'period': '2',
                 'start':  '2010-02-01',
                 'end':    '2010-03-31'},
                {'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-02-28'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-01-31'},
                    {'year':  '2010',
                     'start': '2010-02-01',
                     'end':   '2010-02-28'},
                    {'year':  '2010',
                     'start': '2010-03-01',
                     'end':   '2010-03-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge04a(self):
        """
        Test condense with 2 overlapping intervals and 2 rows (X starts Y).
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-02-28'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-01-01',
                 'end':    '2010-03-31'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-02-28'},
                    {'year':  '2010',
                     'start': '2010-03-01',
                     'end':   '2010-03-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge04b(self):
        """
        Test condense with 2 overlapping intervals adn 3 rows.
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-02-28'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-01-01',
                 'end':    '2010-03-31'},
                {'year':   '2010',
                 'period': '3',
                 'start':  '2010-01-01',
                 'end':    '2010-03-31'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-02-28'},
                    {'year':  '2010',
                     'start': '2010-03-01',
                     'end':   '2010-03-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge05a(self):
        """
        Test condense with 2 overlapping intervals and 2 rows (X during Y).
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-02-01',
                 'end':    '2010-02-28'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-01-01',
                 'end':    '2010-03-31'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-01-31'},
                    {'year':  '2010',
                     'start': '2010-02-01',
                     'end':   '2010-02-28'},
                    {'year':  '2010',
                     'start': '2010-03-01',
                     'end':   '2010-03-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge05b(self):
        """
        Test condense with 2 overlapping intervals and 3 rows.
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-02-01',
                 'end':    '2010-02-28'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-01-01',
                 'end':    '2010-03-31'},
                {'year':   '2010',
                 'period': '3',
                 'start':  '2010-01-01',
                 'end':    '2010-03-31'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-01-31'},
                    {'year':  '2010',
                     'start': '2010-02-01',
                     'end':   '2010-02-28'},
                    {'year':  '2010',
                     'start': '2010-03-01',
                     'end':   '2010-03-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge05c(self):
        """
        Test condense with 2 overlapping intervals and 2 rows (X during Y).
        """
        rows = [{'year':   '2010',
                 'period': '2',
                 'start':  '2010-01-01',
                 'end':    '2010-03-31'},
                {'year':   '2010',
                 'period': '1',
                 'start':  '2010-02-01',
                 'end':    '2010-02-28'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-01-31'},
                    {'year':  '2010',
                     'start': '2010-02-01',
                     'end':   '2010-02-28'},
                    {'year':  '2010',
                     'start': '2010-03-01',
                     'end':   '2010-03-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge06a(self):
        """
        Test condense with 2 overlapping intervals and 2 rows (X finishes Y).
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-03-01',
                 'end':    '2010-03-31'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-01-01',
                 'end':    '2010-03-31'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-02-28'},
                    {'year':  '2010',
                     'start': '2010-03-01',
                     'end':   '2010-03-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge06b(self):
        """
        Test condense with 2 overlapping intervals and 3 rows
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-03-01',
                 'end':    '2010-03-31'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-01-01',
                 'end':    '2010-03-31'},
                {'year':   '2010',
                 'period': '3',
                 'start':  '2010-01-01',
                 'end':    '2010-03-31'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-02-28'},
                    {'year':  '2010',
                     'start': '2010-03-01',
                     'end':   '2010-03-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge06c(self):
        """
        Test condense with 2 overlapping intervals and 2 rows (X finishes Y).
        """
        rows = [{'year':   '2010',
                 'period': '2',
                 'start':  '2010-01-01',
                 'end':    '2010-03-31'},
                {'year':   '2010',
                 'period': '1',
                 'start':  '2010-03-01',
                 'end':    '2010-03-31'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-02-28'},
                    {'year':  '2010',
                     'start': '2010-03-01',
                     'end':   '2010-03-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge07a(self):
        """
        Test condense with 2 equal intervals and 2 rows.
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-01-31'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-01-01',
                 'end':    '2010-01-31'}
                ]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-01-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge07b(self):
        """
        Test condense with 2 equal intervals and 3 rows.
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-01-31'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-01-01',
                 'end':    '2010-01-31'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-01-01',
                 'end':    '2010-01-31'}
                ]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-01-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge8a(self):
        """
        Test with 3 intervals.
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-12-31'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-02-01',
                 'end':    '2010-02-28'},
                {'year':   '2010',
                 'period': '3',
                 'start':  '2010-05-01',
                 'end':    '2010-05-31'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-01-31'},
                    {'year':  '2010',
                     'start': '2010-02-01',
                     'end':   '2010-02-28'},
                    {'year':  '2010',
                     'start': '2010-03-01',
                     'end':   '2010-04-30'},
                    {'year':  '2010',
                     'start': '2010-05-01',
                     'end':   '2010-05-31'},
                    {'year':  '2010',
                     'start': '2010-06-01',
                     'end':   '2010-12-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_merge8b(self):
        """
        Test with 5 intervals.
        """
        rows = [{'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-12-31'},
                {'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-12-31'},
                {'year':   '2010',
                 'period': '1',
                 'start':  '2010-01-01',
                 'end':    '2010-12-31'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-02-01',
                 'end':    '2010-02-28'},
                {'year':   '2010',
                 'period': '2',
                 'start':  '2010-02-01',
                 'end':    '2010-02-28'},
                {'year':   '2010',
                 'period': '3',
                 'start':  '2010-05-01',
                 'end':    '2010-05-31'},
                {'year':   '2010',
                 'period': '3',
                 'start':  '2010-05-01',
                 'end':    '2010-05-31'}]

        expected = [{'year':  '2010',
                     'start': '2010-01-01',
                     'end':   '2010-01-31'},
                    {'year':  '2010',
                     'start': '2010-02-01',
                     'end':   '2010-02-28'},
                    {'year':  '2010',
                     'start': '2010-03-01',
                     'end':   '2010-04-30'},
                    {'year':  '2010',
                     'start': '2010-05-01',
                     'end':   '2010-05-31'},
                    {'year':  '2010',
                     'start': '2010-06-01',
                     'end':   '2010-12-31'}]

        helper = Type2CondenseHelper('start', 'end', ['year'])
        helper.prepare_data(rows)
        actual = helper.condense()
        self._drop_field(actual, 'period')

        self.assertEqual(expected, actual)

# ----------------------------------------------------------------------------------------------------------------------
