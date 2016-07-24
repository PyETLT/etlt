import unittest

from etlt.helper.Type2Helper import Type2Helper


class Type2JoinTest(unittest.TestCase):
    """
    Test cases for Type2Join
    """

    # ------------------------------------------------------------------------------------------------------------------
    def test_enumerate(self):
        """
        Test enumeration of rows.
        """
        rows = [{'a':     1,
                 'b':     2,
                 'c':     3,
                 'start': '2000-03-01',
                 'end':   '2000-03-31'},
                {'a':     1,
                 'b':     2,
                 'c':     3,
                 'start': '2000-02-01',
                 'end':   '2000-02-29'},
                {'a':     1,
                 'b':     2,
                 'c':     3,
                 'start': '2000-01-01',
                 'end':   '2000-12-31'},
                {'a':     1,
                 'b':     2,
                 'c':     3,
                 'start': '2000-01-01',
                 'end':   '2001-01-31'},
                {'a':     1,
                 'b':     2,
                 'c':     4,
                 'start': '2000-03-01',
                 'end':   '2000-03-31'},
                {'a':     1,
                 'b':     2,
                 'c':     4,
                 'start': '2000-02-01',
                 'end':   '2000-02-29'}]
        expected = [{'a':       1,
                     'b':       2,
                     'c':       3,
                     'end':     '2000-12-31',
                     'ordinal': 1,
                     'start':   '2000-01-01'},
                    {'a':       1,
                     'b':       2,
                     'c':       3,
                     'end':     '2001-01-31',
                     'ordinal': 2,
                     'start':   '2000-01-01'},
                    {'a':       1,
                     'b':       2,
                     'c':       3,
                     'end':     '2000-02-29',
                     'ordinal': 3,
                     'start':   '2000-02-01'},
                    {'a':       1,
                     'b':       2,
                     'c':       3,
                     'end':     '2000-03-31',
                     'ordinal': 4,
                     'start':   '2000-03-01'},
                    {'a':       1,
                     'b':       2,
                     'c':       4,
                     'end':     '2000-02-29',
                     'ordinal': 1,
                     'start':   '2000-02-01'},
                    {'a':       1,
                     'b':       2,
                     'c':       4,
                     'end':     '2000-03-31',
                     'ordinal': 2,
                     'start':   '2000-03-01'}]

        helper = Type2Helper('start', 'end', ['a', 'b', 'c'])
        helper.prepare_data(rows)
        helper.enumerate('ordinal')
        actual = helper.get_rows(True)

        self.assertEqual(expected, actual)

# ----------------------------------------------------------------------------------------------------------------------
