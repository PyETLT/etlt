import bz2
import copy
import csv
from itertools import zip_longest
from typing import Dict, List, Optional, Union

import chardet

from etlt.reader.Reader import Reader
from etlt.reader.UniversalCsvReaderFormatHelper import UniversalCsvReaderFormatHelper


class UniversalCsvReader(Reader):
    """
    A universal CSV file reader.
    - Open uncompressed and gz, bz2 compressed files.
    - Auto encoding and field delimiter detection.
    """
    sample_size = 64 * 1024

    line_endings = ['\r\n', '\n\r', '\n', '\r']

    delimiters = [',', ';', '\t', '|', ':']

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, filenames: List[str], format_helper=None):
        """
        Object constructor.

        :param list(str) filenames: A list of CSV file names.
        """
        Reader.__init__(self)

        self._filenames: List[str] = filenames
        """
        The name of the CSV files.
        """

        self._file = None
        """
        The current actual file object.
        """

        self._csv_reader = None
        """
        The current actual CSV file object.

        :type: _csv.reader
        """

        self._mapping: Optional[Dict[str, int]] = None
        """
        The mapping from column names to column numbers.
        """

        self._filename: Optional[str] = None
        """
        The name of the current file.
        """

        self._helper = UniversalCsvReaderFormatHelper() if not format_helper else format_helper
        """
        The helper for detecting the appropriate formatting parameters for reading the current CSV file.
        """

        self._formatting_parameters: Dict[str, str] = dict()
        """
        The CSV formatting parameters for reading the current CSV file.
        """

        self._sample: Optional[Union[str, bytes]] = None
        """
        The sample when detecting automatically formatting parameters.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def __enter__(self):
        # Nothing to do.
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def __exit__(self, *_):
        self._close()

    # ------------------------------------------------------------------------------------------------------------------
    def get_source_name(self) -> Optional[str]:
        """
        Returns the current source file.
        """
        return self._filename

    # ------------------------------------------------------------------------------------------------------------------
    def next(self):
        """
        Yields the next row from the source files.
        """
        for self._filename in self._filenames:
            self._open()
            for row in self._csv_reader:
                self._row_number += 1
                if self._mapping:
                    yield {column_name: row[index] if 0 <= index < len(row) else '' for column_name, index in
                           self._mapping.items()}
                elif self._fields:
                    yield dict(zip_longest(self._fields, row, fillvalue=''))
                else:
                    yield row

            self._close()
            self._row_number = -1

        self._filename = None

        return

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def mapping(self) -> Optional[Dict[str, int]]:
        """
        Getter for mapping.
        """
        return copy.copy(self._mapping)

    # ------------------------------------------------------------------------------------------------------------------
    @mapping.setter
    def mapping(self, mapping: Optional[Dict[str, int]]):
        """

        """
        self._mapping = mapping

    # ------------------------------------------------------------------------------------------------------------------
    def _open_file(self, mode: str, encoding: Optional[str] = None) -> None:
        """
        Opens the next current file.

        :param mode: The mode for opening the file.
        :param encoding: The encoding of the file.
        """
        if self._filename[-4:] == '.bz2':
            self._file = bz2.open(self._filename, mode=mode, encoding=encoding)
        else:
            self._file = open(self._filename, mode=mode, encoding=encoding)

    # ------------------------------------------------------------------------------------------------------------------
    def _close(self) -> None:
        """
        Closes the current file.
        """
        if self._file:
            self._file.close()

    # ------------------------------------------------------------------------------------------------------------------
    def _get_sample(self, mode: str, encoding: Optional[str]) -> None:
        """
        Get a sample from the next current input file.

        :param str mode: The mode for opening the file.
        :param str|None encoding: The encoding of the file. None for open the file in binary mode.
        """
        self._open_file(mode, encoding)
        self._sample = self._file.read(UniversalCsvReader.sample_size)
        self._file.close()

    # ------------------------------------------------------------------------------------------------------------------
    def _detect_encoding(self) -> None:
        """
        Detects the encoding og the current file.
        """
        self._formatting_parameters['encoding'] = chardet.detect(self._sample)['encoding']

    # ------------------------------------------------------------------------------------------------------------------
    def _detect_delimiter(self) -> None:
        """
        Detects the field delimiter in the sample data.
        """
        candidate_value = ','
        candidate_count = 0
        for delimiter in UniversalCsvReader.delimiters:
            count = self._sample.count(delimiter)
            if count > candidate_count:
                candidate_value = delimiter
                candidate_count = count

        self._formatting_parameters['delimiter'] = candidate_value

    # ------------------------------------------------------------------------------------------------------------------
    def _detect_line_ending(self) -> None:
        """
        Detects the line ending in the sample data.
        """
        candidate_value = '\n'
        candidate_count = 0
        for line_ending in UniversalCsvReader.line_endings:
            count = self._sample.count(line_ending)
            if count > candidate_count:
                candidate_value = line_ending
                candidate_count = count

        self._formatting_parameters['line_terminator'] = candidate_value

    # ------------------------------------------------------------------------------------------------------------------
    def _open(self) -> None:
        """
        Opens the next current file with proper settings for encoding and delimiter.
        """
        self._sample = None

        formatting_parameters0 = {
                'encoding':        'auto',
                'delimiter':       'auto',
                'line_terminator': 'auto',
                'escape_char':     '\\',
                'quote_char':      '"'}
        formatting_parameters1 = self._helper.pass1(self._filename, formatting_parameters0)
        self._formatting_parameters = formatting_parameters1

        # Detect encoding.
        if formatting_parameters1['encoding'] == 'auto':
            self._get_sample('rb', None)
            self._detect_encoding()

        # Detect delimiter.
        if formatting_parameters1['delimiter'] == 'auto':
            self._get_sample('rt', formatting_parameters1['encoding'])
            self._detect_delimiter()

        # Detect line terminators.
        if formatting_parameters1['line_terminator'] == 'auto':
            if not self._sample:
                self._get_sample('rt', formatting_parameters1['encoding'])
            self._detect_line_ending()

        self._formatting_parameters = self._helper.pass2(self._filename,
                                                         self._formatting_parameters,
                                                         formatting_parameters1)

        self._open_file('rt', formatting_parameters1['encoding'])
        self._csv_reader = csv.reader(self._file,
                                      delimiter=self._formatting_parameters['delimiter'],
                                      escapechar=self._formatting_parameters['escape_char'],
                                      lineterminator=self._formatting_parameters['line_terminator'],
                                      quotechar=self._formatting_parameters['quote_char'])  # Ignored

        self._sample = None

# ----------------------------------------------------------------------------------------------------------------------
