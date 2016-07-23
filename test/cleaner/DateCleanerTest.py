import unittest

from etlt.cleaner.DateCleaner import DateCleaner


class DateCleanerTest(unittest.TestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def _test(self, expected, dirty):
        clean = DateCleaner.clean(dirty)
        self.assertEqual(expected, clean)

    # ------------------------------------------------------------------------------------------------------------------
    def test00(self):
        self._test('', '')
        self._test('qwerty', 'qwerty')
        self._test('2000-123-123', '2000-123-123')

    # ------------------------------------------------------------------------------------------------------------------
    def test01(self):
        self._test('1966-04-10', '19660410')  # YYYYMMDD format.

    # ------------------------------------------------------------------------------------------------------------------
    def test02(self):
        self._test('1966-04-10', '1966-04-10')  # YYYY-MM-DD format.
        self._test('1971-07-01', '1971-7-1')  # YYYY-M-D format.
        self._test('1966-04-10', '10-04-1966')  # DD-MM-YYYY format.
        self._test('1971-07-01', '1-7-1971')  # D-M-YYYY format.
        self._test('1966-04-10', '10-04-66')  # DD-MM-YY format.
        self._test('1971-07-01', '1-7-71')  # D-M-YY format.

    # ------------------------------------------------------------------------------------------------------------------
    def test03(self):
        self._test('1966-04-10', '1966.04.10')  # YYYY.MM.DD format.
        self._test('1971-07-01', '1971.7.1')  # YYYY.M.D format.
        self._test('1966-04-10', '10.04.1966')  # DD.MM.YYYY format.
        self._test('1971-07-01', '1.7.1971')  # D.M.YYYY format.
        self._test('1966-04-10', '10.04.66')  # DD.MM.YY format.
        self._test('1971-07-01', '1.7.71')  # D.M.YY format.

    # ------------------------------------------------------------------------------------------------------------------
    def test04(self):
        self._test('1966-04-10', '1966/04/10')  # YYYY/MM/DD format
        self._test('1971-07-01', '1971/7/1')  # YYYY/M/D format.
        self._test('1966-04-10', '10/04/1966')  # DD/MM/YYYY format.
        self._test('1971-07-01', '1/7/1971')  # D/M/YYYY format.
        self._test('1966-04-10', '10/04/66')  # DD/MM/YY format.
        self._test('1971-07-01', '1/7/71')  # D/M/YY format.

    # ------------------------------------------------------------------------------------------------------------------
    def test05(self):
        self._test('1966-04-10', '1966 04 10')  # YYYY MM DD format
        self._test('1971-07-01', '1971 7 1')  # YYYY M D format.
        self._test('1966-04-10', '10 04 1966')  # DD MM YYYY format.
        self._test('1971-07-01', '1 7 1971')  # D M YYYY format.
        self._test('1966-04-10', '10 04 66')  # DD MM YY format.
        self._test('1971-07-01', '1 7 71')  # D M YY format.

# ----------------------------------------------------------------------------------------------------------------------
