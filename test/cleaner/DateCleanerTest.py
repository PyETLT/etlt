import unittest

from etlt.cleaner.DateCleaner import DateCleaner


class DateCleanerTest(unittest.TestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def _test(self, expected, dirty, ignore_time=False):
        clean = DateCleaner.clean(dirty, ignore_time)
        self.assertEqual(expected, clean)

    # ------------------------------------------------------------------------------------------------------------------
    def test00(self):
        """
        Tests with string that are not a date at all.
        """
        self._test('', '')
        self._test('qwerty', 'qwerty')
        self._test('2000-123-123', '2000-123-123')

    # ------------------------------------------------------------------------------------------------------------------
    def test01(self):
        """
        Tests without a separator.
        """
        self._test('1966-04-10', '19660410')  # YYYYMMDD format.

    # ------------------------------------------------------------------------------------------------------------------
    def test02(self):
        """
        Tests without a dash as separator.
        """
        self._test('1966-04-10', '1966-04-10')  # YYYY-MM-DD format.
        self._test('1971-07-01', '1971-7-1')  # YYYY-M-D format.
        self._test('1966-04-10', '10-04-1966')  # DD-MM-YYYY format.
        self._test('1971-07-01', '1-7-1971')  # D-M-YYYY format.
        self._test('1966-04-10', '10-04-66')  # DD-MM-YY format.
        self._test('1971-07-01', '1-7-71')  # D-M-YY format.

    # ------------------------------------------------------------------------------------------------------------------
    def test03(self):
        """
        Tests without a dot as separator.
        """
        self._test('1966-04-10', '1966.04.10')  # YYYY.MM.DD format.
        self._test('1971-07-01', '1971.7.1')  # YYYY.M.D format.
        self._test('1966-04-10', '10.04.1966')  # DD.MM.YYYY format.
        self._test('1971-07-01', '1.7.1971')  # D.M.YYYY format.
        self._test('1966-04-10', '10.04.66')  # DD.MM.YY format.
        self._test('1971-07-01', '1.7.71')  # D.M.YY format.

    # ------------------------------------------------------------------------------------------------------------------
    def test04(self):
        """
        Tests without a dot slash separator.
        """
        self._test('1966-04-10', '1966/04/10')  # YYYY/MM/DD format
        self._test('1971-07-01', '1971/7/1')  # YYYY/M/D format.
        self._test('1966-04-10', '10/04/1966')  # DD/MM/YYYY format.
        self._test('1971-07-01', '1/7/1971')  # D/M/YYYY format.
        self._test('1966-04-10', '10/04/66')  # DD/MM/YY format.
        self._test('1971-07-01', '1/7/71')  # D/M/YY format.

    # ------------------------------------------------------------------------------------------------------------------
    def test05(self):
        """
        Tests without a space as separator.
        """
        self._test('1966-04-10', '1966 04 10')  # YYYY MM DD format
        self._test('1971-07-01', '1971 7 1')  # YYYY M D format.
        self._test('1966-04-10', '10 04 1966')  # DD MM YYYY format.
        self._test('1971-07-01', '1 7 1971')  # D M YYYY format.
        self._test('1966-04-10', '10 04 66')  # DD MM YY format.
        self._test('1971-07-01', '1 7 71')  # D M YY format.

    # ------------------------------------------------------------------------------------------------------------------
    def test06(self):
        """
        Tests with trailing midnight time.
        """
        self._test('1966-04-10', '1966-04-10 00:00:00')
        self._test('1966-04-10', '10-4-1966 0:00:00')
        self._test('1966-04-10', '1966-04-10 00:00:00.000')

        self._test('1966-04-10', '1966.04.10 00:00:00')
        self._test('1966-04-10', '10.4.1966 0:00:00')
        self._test('1966-04-10', '1966.04.10 00:00:00.000')

    # ------------------------------------------------------------------------------------------------------------------
    def test07(self):
        """
        Tests with trailing time.
        """
        self._test('1966-04-10', '1966-04-10 23:23:23', True)
        self._test('1966-04-10', '10-4-1966 3:23:23', True)
        self._test('1966-04-10', '1966-04-10 23:23:23.231', True)
        self._test('1966-04-10', '1966-04-10 everything after the date is ignored', True)

        self._test('1966-04-10', '1966.04.10 23:23:23', True)
        self._test('1966-04-10', '10.4.1966 3:23:23', True)
        self._test('1966-04-10', '1966.04.10 23:23:23.231', True)
        self._test('1966-04-10', '1966.04.10 everything after the date is ignored', True)

# ----------------------------------------------------------------------------------------------------------------------
