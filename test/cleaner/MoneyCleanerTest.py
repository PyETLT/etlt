import unittest

from etlt.cleaner.MoneyCleaner import MoneyCleaner


class MoneyCleanerTest(unittest.TestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def _test(self, expected, dirty):
        clean = MoneyCleaner.clean(dirty)
        self.assertEqual(expected, clean)

    # ------------------------------------------------------------------------------------------------------------------
    def test00(self):
        """
        Tests with non valid amounts.
        """
        self._test('', '')
        self._test('qwerty', 'qwerty')

    # ------------------------------------------------------------------------------------------------------------------
    def test01(self):
        """
        Test with Dutch formats and thousand separators.
        """
        self._test('1123.1', '1.123,1')
        self._test('1123', '1.123')
        self._test('1123.1', '1 123,1')
        self._test('1123.12', '1.123,12')
        self._test('1123.12', '1 123,12')
        self._test('1123', '1 123')

    # ------------------------------------------------------------------------------------------------------------------
    def test02(self):
        """
        Test with English formats and thousands separators.
        """
        self._test('1123.1', '1,123.1')
        self._test('1123.1', '1 123.1')
        self._test('1123.12', '1,123.12')
        self._test('1123.12', '1 123.12')

    # ------------------------------------------------------------------------------------------------------------------
    def test03(self):
        """
        Tests with decimal point and commas without thousand separators.
        """
        self._test('123.1', '123.1')
        self._test('123.1', '123,1')
        self._test('123.12', '123.12')
        self._test('123.12', '123,12')

    # ------------------------------------------------------------------------------------------------------------------
    def test04(self):
        """
        Tests with decimal point and commas without thousands separators.
        """
        self._test('1451.3', '1451.3')
        self._test('1451.3', '1451,3')
        self._test('1451.37', '1451.37')
        self._test('1451.37', '1451,37')

    # ------------------------------------------------------------------------------------------------------------------
    def test05(self):
        """
        Tests with ambiguous formats.
        """
        self._test('123.123', '123.123')
        self._test('123,123', '123,123')

# ----------------------------------------------------------------------------------------------------------------------
