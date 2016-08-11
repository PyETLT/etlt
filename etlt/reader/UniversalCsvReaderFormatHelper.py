"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""


class UniversalCsvReaderFormatHelper:
    """
    A helper class for UniversalCsvReader for setting and correcting the formatting parameters for reading CSV files.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def pass1(self, filename, formatting_parameters0):
        """
        Returns the formatting parameters for reading the next current CSV file.

        This method is called by UniversalCsvReader before opening the CSV file and before auto detecting parameters.

        Override this method in your own child class according to your needs.

        :param str filename: The next current file name.
        :param dict[str,str] formatting_parameters0: The default formatting parameters. Keys are:
                                                     - encoding: Use auto for auto detecting.
                                                     - delimiter: Use auto for auto detecting.
                                                     - line_terminator: Use auto for auto detecting.
                                                     - escape_char
                                                     - quote_char

        :rtype: dict[str,str]
        """
        return formatting_parameters0

    # ------------------------------------------------------------------------------------------------------------------
    def pass2(self, filename, formatting_parameters1, formatting_parameters2):
        """
        Returns the formatting parameters for reading the next current CSV file.

        This method is called by UniversalCsvReader after auto detecting parameters.

        Override this method in your own child class according to your needs.

        :param str filename: The next current file name.
        :param dict[str,str] formatting_parameters1: The formatting parameters as returned by pass1.
        :param dict[str,str] formatting_parameters2: The formatting parameters as returned by pass1 but parameters set
                                                     to auto are replaced with the automatically detected values.

        :rtype: dict[str,str]
        """
        return formatting_parameters2

# ----------------------------------------------------------------------------------------------------------------------
