import unittest

from etlt.condition.InListCondition import InListCondition


class InListConditionTest(unittest.TestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def test01(self) -> None:
        """
        Test InListCondition with various expressions and values.
        """
        my_filter = InListCondition('word')
        expressions = [{'condition': 'spam'},
                       {'condition': 'plain:eggs'},
                       {'condition': 'glob:abc*'},
                       {'condition': 're:python$'}]
        my_filter.populate_values(expressions, 'condition')

        self.assertTrue(my_filter.match({'word': 'spam'}), 'spam')
        self.assertFalse(my_filter.match({'word': 'SPAM'}), 'SPAM')
        self.assertTrue(my_filter.match({'word': 'eggs'}), 'eggs')
        self.assertFalse(my_filter.match({'word': 'EGGS'}), 'EGGS')
        self.assertTrue(my_filter.match({'word': 'abc'}), 'abc')
        self.assertTrue(my_filter.match({'word': 'abcd'}), 'abcd')
        self.assertTrue(my_filter.match({'word': 'abcdef'}), 'abcdef')
        self.assertTrue(my_filter.match({'word': 'python'}), 'python')
        self.assertTrue(my_filter.match({'word': 'monty python'}), 'monty python')
        self.assertFalse(my_filter.match({'word': 'foo'}), 'foo')
        self.assertFalse(my_filter.match({'word': 'bar'}), 'bar')

# ----------------------------------------------------------------------------------------------------------------------
