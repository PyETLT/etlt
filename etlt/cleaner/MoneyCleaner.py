import re


class MoneyCleaner:
    """
    Utility class for converting numbers to numbers with decimal points.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def clean(amount):
        """
        Converts a number to a number with decimal point.

        :param str amount: The input number.

        :rtype str:
        """
        # Return empty input immediately.
        if not amount:
            return amount

        if re.match('[\. ][0-9]{3},[0-9]{2}$', amount):
            # Assume amount is in 1.123,12 or 1 123,12 format (Dutch).
            amount.replace('.', '').replace(' ', '').replace(',', '.')

            return amount

        if re.match('[, ][0-9]{3}\.[0-9]{2}$', amount):
            # Assume amount is in 1,123.12 or in 1 123.12 format (Engels).
            amount.replace('.', '').replace(' ', '').replace(',', '.')

            return amount

        if re.match('[0-9](,[0-9]{2}$)', amount):
            # Assume amount is in 123,12 format (Dutch).
            amount.replace(',', '.')

            return amount

        # Format of amount is not recognized. Return amount.
        return amount

# ----------------------------------------------------------------------------------------------------------------------
