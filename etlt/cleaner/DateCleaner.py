import re
from typing import Optional


class DateCleaner:
    """
    Utility class for converting dates in miscellaneous formats to ISO-8601 (YYYY-MM-DD) format.
    """

    # ------------------------------------------------------------------------------------------------------------------
    month_map = {
            # English
            'jan': '01',
            'feb': '02',
            'mar': '03',
            'apr': '04',
            'may': '05',
            'jun': '06',
            'jul': '07',
            'aug': '08',
            'sep': '09',
            'oct': '10',
            'nov': '11',
            'dec': '12',

            # Dutch
            'mrt': '03',
            'mei': '05',
            'okt': '10'
    }

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def clean(date: Optional[str], ignore_time: bool = False) -> Optional[str]:
        """
        Converts a date in miscellaneous format to ISO-8601 (YYYY-MM-DD) format.

        :param date: The input date.
        :param ignore_time: Whether any trailing time part must be ignored.
        """
        # Return empty input immediately.
        if not date:
            return date

        parts = re.split(r'[\-/. ]', date)

        if (len(parts) == 3) or \
                (len(parts) > 3 and ignore_time) or \
                (len(parts) == 4 and re.match(r'^[0:]*$', parts[3])) or \
                (len(parts) == 5 and re.match(r'^[0:]*$', parts[3]) and re.match(r'^0*$', parts[4])):
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

        # Try DD-MM-YYYY HH:mm:ss format
        pattern = r'^(\d{2})\D(\d{2})\D(\d{4})' + ('.*$' if ignore_time else r'(\D(\d{1,2})\D(\d{1,2})\D(\d{1,2}))?$')
        match = re.match(pattern, date)
        if match:
            ret = match.group(3) + '-' + match.group(2) + '-' + match.group(1)
            if len(match.groups()) == 7 and match.group(4):
                ret += 'T' + match.group(5) + ':' + match.group(6) + ':' + match.group(7)
            return ret

        # Try DD-MM-YYYY HH:mm format
        pattern = r'^(\d{2})\D(\d{2})\D(\d{4})' + ('.*$' if ignore_time else r'(\D(\d{1,2})\D(\d{1,2}))?$')
        match = re.match(pattern, date)
        if match:
            ret = match.group(3) + '-' + match.group(2) + '-' + match.group(1)
            if len(match.groups()) == 6 and match.group(4):
                ret += 'T' + match.group(5) + ':' + match.group(6) + ':00'
            return ret

        # Try DDmonYYYY or DDmonYYYY HH:mm:ss format
        pattern = r'^(\d{2})([a-z]{3})(\d{4})' + ('.*$' if ignore_time else r'(\D(\d{1,2})\D(\d{1,2})\D(\d{1,2}))?$')
        match = re.match(pattern, date.lower())
        if match and match.group(2) in DateCleaner.month_map:
            ret = match.group(3) + '-' + DateCleaner.month_map[match.group(2)] + '-' + match.group(1)
            if len(match.groups()) == 7 and match.group(4):
                ret += 'T' + match.group(5) + ':' + match.group(6) + ':' + match.group(7)
            return ret

        # Try YYYYMMDD format.
        pattern = r'^\d{8}' + ('.*$' if ignore_time else '$')
        match = re.match(pattern, date)
        if match:
            # Assume date is YYYYMMDD format
            return date[0:4] + '-' + date[4:6] + '-' + date[6:8]

        # Format not recognized. Just return the original string.
        return date

# ----------------------------------------------------------------------------------------------------------------------
