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

        :param amount: The input number.
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

        if re.search(r'^[0-9]{0,2}(\.[0-9]{3})+(\.[0-9]{2})?$', amount):
            # Amount is in 1.123.12 format.
            return amount.replace('.', '', 1)

        # Format of amount is not recognized. Return amount.
        return amount

# ----------------------------------------------------------------------------------------------------------------------
