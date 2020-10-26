import re
from typing import Optional


class MoneyCleaner:
    """
    Utility class for converting numbers to numbers with decimal points.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def clean(amount: Optional[str]) -> Optional[str]:
        """
        Converts a number to a number with decimal point.

        :param str|None amount: The input number.

        :rtype: str|None
        """
        # Return empty input immediately.
        if not amount:
            return amount

        if re.search(r'^[0-9]{0,2}([. ][0-9]{3})+(,[0-9]{1,2})?$', amount):
            # Assume amount is in 1.123,12 or 1 123,12 or 1 123 format (Dutch).
            return amount.replace('.', '').replace(' ', '').replace(',', '.')

        if re.search(r'^[0-9]{0,2}([, ][0-9]{3})+(\.[0-9]{1,2})?$', amount):
            # Assume amount is in 1,123.12 or 1 123 format (Engels).
            return amount.replace(',', '').replace(' ', '')

        if re.search(r'^[0-9]+(,[0-9]{1,2}$)', amount):
            # Assume amount is in 123,12 or in 123,1 format (Dutch).
            return amount.replace(',', '.')

        # Format of amount is not recognized. Return amount.
        return amount

# ----------------------------------------------------------------------------------------------------------------------
