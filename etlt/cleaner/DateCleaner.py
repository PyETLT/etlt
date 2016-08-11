"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import re


class DateCleaner:
    """
    Utility class for converting dates in miscellaneous formats to ISO-8601 (YYYY-MM-DD) format.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def clean(date):
        """
        Converts a date in miscellaneous format to ISO-8601 (YYYY-MM-DD) format.

        :param str date: The input date.
        :rtype: str
        """
        # Return empty input immediately.
        if not date:
            return date

        parts = re.split(r'[\-/. ]', date)

        if len(parts) == 3 or (len(parts) == 4 and (parts[3] in ('00:00:00', '0:00:00'))):
            if len(parts[0]) == 4 and len(parts[1]) <= 2 and len(parts[2]) <= 2:
                # Assume date is in  YYYY-MM-DD of YYYY-M-D format.
                return parts[0] + '-' + ('00' + parts[1])[-2:] + '-' + ('00' + parts[2])[-2:]

            if len(parts[0]) <= 2 and len(parts[1]) <= 2 and len(parts[2]) == 4:
                # Assume date is in  DD-MM-YYYY or D-M-YYYY format.
                return parts[2] + '-' + ('00' + parts[1])[-2:] + '-' + ('00' + parts[0])[-2:]

            if len(parts[0]) <= 2 and len(parts[1]) <= 2 and len(parts[2]) == 2:
                # Assume date is in  DD-MM-YY or D-M-YY format.
                year = '19' + parts[2] if parts[2] >= '20' else '20' + parts[2]

                return year + '-' + ('00' + parts[1])[-2:] + '-' + ('00' + parts[0])[-2:]

        if len(parts) == 1 and len(date) == 8:
            # Assume date is in YYYYMMDD format.
            return date[0:4] + '-' + date[4:6] + '-' + date[6:8]

        # Format not recognized. Just return the original string.
        return date

# ----------------------------------------------------------------------------------------------------------------------
