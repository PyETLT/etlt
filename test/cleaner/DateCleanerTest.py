import unittest

from etlt.cleaner.DateCleaner import DateCleaner


class DateCleanerTest(unittest.TestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def _test(self, expected, dirty, ignore_time=False):
        clean = DateCleaner.clean(dirty, ignore_time)
        self.assertEqual(expected, clean)

    # ------------------------------------------------------------------------------------------------------------------
    def test00(self) -> None:
        """
        Tests with string that are not a date at all.
        """
        self._test('', '')
        self._test('qwerty', 'qwerty')
        self._test('2000-123-123', '2000-123-123')

    # ------------------------------------------------------------------------------------------------------------------
    def test01a(self) -> None:
        """
        Tests without a separator.
        """
        self._test('1966-04-10', '19660410')  # YYYYMMDD format.
        self._test('2014-01-02', '02jan2014')  # DDmonYYYY format.
        self._test('2014-01-03', '03JAN2014')  # DDMONYYYY format.
        self._test('2014-01-02T14:15:00', '02jan2014:14:15:00')  # DDmonYYYY HH:mm:ssformat.
        self._test('2014-01-03T14:15:00', '03JAN2014:14:15:00')  # DDMONYYYY HH:mm:ssformat.

    # ------------------------------------------------------------------------------------------------------------------
    def test01b(self) -> None:
        """
        Tests without a separator ignoring time.
        """
        self._test('1966-04-10', '19660410 141500', True)  # YYYYMMDD format.
        self._test('2014-01-02', '02jan2014:14:15:00', True)  # DDmonYYYY format.
        self._test('2014-01-03', '03JAN2014:14:15:00', True)  # DDMONYYYY format.
        self._test('2014-01-02', '02jan2014:14:15:00', True)  # DDmonYYYY HH:mm:ssformat.
        self._test('2014-01-03', '03JAN2014:14:15:00', True)  # DDMONYYYY HH:mm:ssformat.

    # ------------------------------------------------------------------------------------------------------------------
    def test02(self) -> None:
        """
        Tests with a dash as separator.
        """
        self._test('1966-04-10', '1966-04-10')  # YYYY-MM-DD format.
        self._test('1971-07-01', '1971-7-1')  # YYYY-M-D format.
        self._test('1966-04-10', '10-04-1966')  # DD-MM-YYYY format.
        self._test('1971-07-01', '1-7-1971')  # D-M-YYYY format.
        self._test('1966-04-10', '10-04-66')  # DD-MM-YY format.
        self._test('1971-07-01', '1-7-71')  # D-M-YY format.

    # ------------------------------------------------------------------------------------------------------------------
    def test03(self) -> None:
        """
        Tests with a dot as separator.
        """
        self._test('1966-04-10', '1966.04.10')  # YYYY.MM.DD format.
        self._test('1971-07-01', '1971.7.1')  # YYYY.M.D format.
        self._test('1966-04-10', '10.04.1966')  # DD.MM.YYYY format.
        self._test('1971-07-01', '1.7.1971')  # D.M.YYYY format.
        self._test('1966-04-10', '10.04.66')  # DD.MM.YY format.
        self._test('1971-07-01', '1.7.71')  # D.M.YY format.

    # ------------------------------------------------------------------------------------------------------------------
    def test04(self) -> None:
        """
        Tests with a slash separator.
        """
        self._test('1966-04-10', '1966/04/10')  # YYYY/MM/DD format
        self._test('1971-07-01', '1971/7/1')  # YYYY/M/D format.
        self._test('1966-04-10', '10/04/1966')  # DD/MM/YYYY format.
        self._test('1971-07-01', '1/7/1971')  # D/M/YYYY format.
        self._test('1966-04-10', '10/04/66')  # DD/MM/YY format.
        self._test('1971-07-01', '1/7/71')  # D/M/YY format.

    # ------------------------------------------------------------------------------------------------------------------
    def test05(self) -> None:
        """
        Tests with a space as separator.
        """
        self._test('1966-04-10', '1966 04 10')  # YYYY MM DD format
        self._test('1971-07-01', '1971 7 1')  # YYYY M D format.
        self._test('1966-04-10', '10 04 1966')  # DD MM YYYY format.
        self._test('1971-07-01', '1 7 1971')  # D M YYYY format.
        self._test('1966-04-10', '10 04 66')  # DD MM YY format.
        self._test('1971-07-01', '1 7 71')  # D M YY format.

    # ------------------------------------------------------------------------------------------------------------------
    def test06(self) -> None:
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
    def test07(self) -> None:
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
