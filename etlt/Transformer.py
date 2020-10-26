import abc
import copy
import re
import time
import traceback
from typing import Any, Dict, List

from etlt.cleaner.WhitespaceCleaner import WhitespaceCleaner
from etlt.reader.Reader import Reader
from etlt.writer.SqlLoaderWriter import SqlLoaderWriter


class Transformer(metaclass=abc.ABCMeta):
    """
    Abstract parent class for transforming source data in (partial) dimensional data.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 source_reader: Reader,
                 transformed_writer: SqlLoaderWriter,
                 parked_writer: SqlLoaderWriter,
                 ignored_writer: SqlLoaderWriter):
        """
        Object constructor.

        :param Reader source_reader: Object for reading source rows.
        :param SqlLoaderWriter transformed_writer: Object for writing successfully transformed rows.
        :param SqlLoaderWriter parked_writer: Object for writing parked rows.
        :param SqlLoaderWriter ignored_writer: Object for writing ignored rows.
        """

        self._count_total: int = 0
        """
        The number of rows processed.
        """

        self._count_transform: int = 0
        """
        The number of rows successfully transformed.
        """

        self._count_park: int = 0
        """
        The number of rows parked.
        """

        self._count_error: int = 0
        """
        The number of rows processed with errors.
        """

        self._count_ignore: int = 0
        """
        The number of rows ignored.
        """

        self._time0: float = 0.0
        """
        Start time of the whole process and start of transforming rows.
        """

        self._time1: float = 0.0
        """
        End time of transforming rows and start time of the loading transformed rows.
        """

        self._time2: float = 0.0
        """
        End time of the loading transformed rows and start time of loading parked rows.
        """

        self._time3: float = 0.0
        """
        End time of the loading parked rows and end time of the whole process.
        """

        self._source_reader: Reader = source_reader
        """
        Object for reading source rows.
        """

        self._transformed_writer: SqlLoaderWriter = transformed_writer
        """
        Object for writing successfully transformed rows.r
        """

        self._parked_writer: SqlLoaderWriter = parked_writer
        """
        Object for writing parked rows.
        """

        self._ignored_writer: SqlLoaderWriter = ignored_writer
        """
        Object for writing ignored rows.
        """

        self._mandatory_fields: List[str] = []
        """
        The mandatory fields (or columns) in the output row.
        """

        self._steps: List[callable] = []
        """
        All _step<n> methods where n is an integer in this class sorted by n.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _log(message):
        """
        Logs a message.

        :param str message: The log message.

        :rtype: None
        """
        #  @todo Replace with log package.
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' ' + str(message), flush=True)

    # ------------------------------------------------------------------------------------------------------------------
    def _handle_exception(self, row, exception) -> None:
        """
        Logs an exception occurred during transformation of a row.

        :param list|dict|() row: The source row.
        :param Exception exception: The exception.
        """
        self._log('Error during processing of line {0:d}.'.format(self._source_reader.row_number))
        self._log(row)
        self._log(str(exception))
        self._log(traceback.format_exc())

    # ------------------------------------------------------------------------------------------------------------------
    def _find_all_step_methods(self) -> None:
        """
        Finds all _step<n> methods where n is an integer in this class.
        """
        steps = ([method for method in dir(self) if callable(getattr(self, method)) and
                  re.match(r'_step\d+\d+.*', method)])
        steps = sorted(steps)
        for step in steps:
            self._steps.append(getattr(self, step))

    # ------------------------------------------------------------------------------------------------------------------
    def _transform_rows(self) -> None:
        """
        Transforms all source rows.
        """
        self._find_all_step_methods()

        for row in self._source_reader.next():
            self._transform_row_wrapper(row)

    # ------------------------------------------------------------------------------------------------------------------
    def pre_park_row(self, park_info, in_row) -> None:
        """
        This method will be called just be for sending an input row to be parked to the parked writer.

        :param str park_info: The park info.
        :param dict[str,str] in_row: The original input row.

        :rtype: None
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def pre_ignore_row(self, ignore_info, in_row) -> None:
        """
        This method will be called just be for sending an input row to be ignored to the ignore writer.

        :param str ignore_info: The ignore info.
        :param dict[str,str] in_row: The original input row.

        :rtype: None
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def _transform_row_wrapper(self, row: Dict[str, Any]) -> None:
        """
        Transforms a single source row.

        :param dict[str,any] row: The source row.
        """
        self._count_total += 1

        try:
            # Transform the naturals keys in line to technical keys.
            in_row = copy.copy(row)
            out_row = {}
            park_info, ignore_info = self._transform_row(in_row, out_row)

        except Exception as e:
            # Log the exception.
            self._handle_exception(row, e)
            # Keep track of the number of errors.
            self._count_error += 1
            # This row must be parked.
            park_info = 'Exception'
            # Keep our IDE happy.
            ignore_info = None
            out_row = {}

        if park_info:
            # Park the row.
            self.pre_park_row(park_info, row)
            self._parked_writer.writerow(row)
            self._count_park += 1
        elif ignore_info:
            # Ignore the row.
            self.pre_ignore_row(ignore_info, row)
            self._ignored_writer.writerow(row)
            self._count_ignore += 1
        else:
            # Write the technical keys and measures to the output file.
            self._transformed_writer.writerow(out_row)
            self._count_transform += 1

    # ------------------------------------------------------------------------------------------------------------------
    def _transform_row(self, in_row, out_row):
        """
        Transforms an input row to an output row (i.e. (partial) dimensional data).

        :param dict[str,str] in_row: The input row.
        :param dict[str,T] out_row: The output row.

        :rtype: (str,str)
        """
        tmp_row = {}

        for step in self._steps:
            park_info, ignore_info = step(in_row, tmp_row, out_row)
            if park_info or ignore_info:
                return park_info, ignore_info

        return None, None

    # ------------------------------------------------------------------------------------------------------------------
    def _step00(self, in_row, tmp_row, out_row):
        """
        Prunes whitespace for all fields in the input row.

        :param dict in_row: The input row.
        :param dict tmp_row: Not used.
        :param dict out_row: Not used.
        """
        for key, value in in_row.items():
            in_row[key] = WhitespaceCleaner.clean(value)

        return None, None

    # ------------------------------------------------------------------------------------------------------------------
    def _step99(self, in_row, tmp_row, out_row):
        """
        Validates all mandatory fields are in the output row and are filled.

        :param dict in_row: The input row.
        :param dict tmp_row: Not used.
        :param dict out_row: The output row.
        """
        park_info = ''
        for field in self._mandatory_fields:
            if field not in out_row or not out_row[field]:
                if park_info:
                    park_info += ' '
                park_info += field

        return park_info, None

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _load_ignored_rows(self) -> None:
        """
        Loads the ignored rows into the database.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _load_parked_rows(self) -> None:
        """
        Loads the parked rows into the database.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _load_transformed_rows(self) -> None:
        """
        Loads the successfully transformed rows into the database.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _log_statistics(self) -> None:
        """
        Log statistics about the number of rows and number of rows per second.
        """
        rows_per_second_trans = self._count_total / (self._time1 - self._time0)
        rows_per_second_load = self._count_transform / (self._time2 - self._time1)
        rows_per_second_overall = self._count_total / (self._time3 - self._time0)

        self._log('Number of rows processed            : {0:d}'.format(self._count_total))
        self._log('Number of rows transformed          : {0:d}'.format(self._count_transform))
        self._log('Number of rows ignored              : {0:d}'.format(self._count_ignore))
        self._log('Number of rows parked               : {0:d}'.format(self._count_park))
        self._log('Number of errors                    : {0:d}'.format(self._count_error))
        self._log('Number of rows per second processed : {0:d}'.format(int(rows_per_second_trans)))
        self._log('Number of rows per second loaded    : {0:d}'.format(int(rows_per_second_load)))
        self._log('Number of rows per second overall   : {0:d}'.format(int(rows_per_second_overall)))

    # ------------------------------------------------------------------------------------------------------------------
    def pre_transform_source_rows(self) -> None:
        """
        This method will be called just before transforming the source rows.

        :rtype: None
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def transform_source_rows(self) -> None:
        """
        Transforms the rows for the source system into (partial) dimensional data.
        """
        # Start timer for overall progress.
        self._time0 = time.perf_counter()

        self.pre_transform_source_rows()

        # Transform all source rows.
        with self._source_reader:
            with self._transformed_writer:
                with self._parked_writer:
                    with self._ignored_writer:
                        self._transform_rows()

        # Time end of transformation.
        self._time1 = time.perf_counter()

        # Load transformed rows into the fact table.
        self._load_transformed_rows()

        # Time end of loading transformed rows.
        self._time2 = time.perf_counter()

        # Load parked and ignored rows into the parked and ignored rows.
        self._load_ignored_rows()
        self._load_parked_rows()

        # Time end of loading parked and ignored rows.
        self._time3 = time.perf_counter()

        # Show statistics about number of rows and performance.
        self._log_statistics()

# ----------------------------------------------------------------------------------------------------------------------
