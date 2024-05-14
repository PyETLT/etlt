from typing import Optional


class WhitespaceCleaner:
    """
    Utility class for cleaning whitespace from strings.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def clean(string: Optional[str]) -> Optional[str]:
        """
        Prunes whitespace from a string.

        :param string: The string.
        """
        # Return empty input immediately.
        if not string:
            return string

        return string.replace('  ', ' ').strip()

# ----------------------------------------------------------------------------------------------------------------------
