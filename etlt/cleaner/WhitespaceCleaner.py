"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""


class WhitespaceCleaner:
    """
    Utility class for cleaning whitespace from strings.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def clean(string):
        """
        Prunes whitespace from a string.

        :param str string: The string.

        :rtype str:
        """
        # Return empty input immediately.
        if not string:
            return string

        return string.replace('  ', ' ').strip()

# ----------------------------------------------------------------------------------------------------------------------
