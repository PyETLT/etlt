"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import abc
import time
import traceback


class Transformer:
    """
    Abstract parent class for transforming source data in (partial) dimensional data.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, source_reader, transformed_writer, parked_writer, ignored_writer):
        """
        Object constructor.

        :param Reader source_reader: Object for reading source rows.
        :param Writer transformed_writer: Object for writing successfully transformed rows.
        :param Writer parked_writer: Object for writing parked rows.
        :param Writer ignored_writer: Object for writing ignored rows.
        """

        self._count_total = 0
        """
        The number of rows processed.

        :type: int
        """

        self._count_transform = 0
        """
        The number of rows successfully transformed.

        :type: int
        """

        self._count_park = 0
        """
        The number of rows parked.

        :type: int
        """

        self._count_error = 0
        """
        The number of rows processed with errors.

        :type: int
        """

        self._count_ignore = 0
        """
        The number of rows ignored.

        :type: int
        """

        self._time0 = 0.0
        """
        Start time of the whole process and start of transforming rows.

        :type: float
        """

        self._time1 = 0.0
        """
        End time of transforming rows and start time of the loading transformed rows.

        :type: float
        """

        self._time2 = 0.0
        """
        End time of the loading transformed rows and start time of loading parked rows.

        :type: float
        """

        self._time3 = 0.0
        """
        End time of the loading parked rows and end time of the whole process.

        :type: float
        """

        self._source_reader = source_reader
        """
        Object for reading source rows.

        :type: etlt.Reader.Reader
        """

        self._transformed_writer = transformed_writer
        """
        Object for writing successfully transformed rows.

        :type: etlt.Writer.Writer
        """

        self._parked_writer = parked_writer
        """
        Object for writing parked rows.

        :type: etlt.Writer.Writer
        """

        self._ignored_write = ignored_writer
        """
        Object for writing ignored rows.

        :type: etlt.Writer.Writer
        """

        # The dimension keys in the output row.
        self.keys = ()

    # ------------------------------------------------------------------------------------------------------------------
    def _log(self, message):
        """
        Logs a message.

        :param str message: The log message.

        :rtype None:
        """
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' ' + str(message))

    # ------------------------------------------------------------------------------------------------------------------
    def _test_dimension_keys(self, output):
        """
        Tests whether all dimension keys are found. Returns a tuple with a bool indicating the row must be parked and
        the names of the missing dimension keys.

        :param list output: The transformed row.

        :rtype: (bool, str)
        """
        park = False
        park_info = ''
        i = 0
        n = len(self.keys)
        while i < n:
            if output[i] is None:
                park = True
                park_info += ' ' if park_info != '' else ''
                park_info += self.keys[i]
            i += 1

        return park, park_info

    # ------------------------------------------------------------------------------------------------------------------
    def _log_exception(self, row, exception):
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
    def _transform_row_wrapper(self, row):
        """
        Transforms a single source row.

        :param list|dict|() row: The source row.
        """
        self._count_total += 1

        try:
            # Transform the naturals keys in line to technical keys.
            output = self._transform_row(row)

            # Test all dimension keys are found.
            park, park_info = self._test_dimension_keys(output)

        except Exception as e:
            # Log the exception.
            self._log_exception(row, e)
            # Keep track of the number of errors.
            self._count_error += 1
            # This row must be parked.
            park = True
            park_info = 'Exception'
            # Keep our IDE happy.
            output = []

        if park:
            # Park the row.
            park = [park_info, self._source_reader.get_source_name, self._source_reader.row_number] + row
            self._parked_writer.put_row(park)
            self._count_park += 1
        else:
            # Write the technical keys and measures to the output file.
            self._transformed_writer.put_row(output)
            self._count_transform += 1

    # ------------------------------------------------------------------------------------------------------------------
    def _transform_rows(self):
        """
        Transforms all source rows.
        """
        row = self._source_reader.get_row()
        while row:
            self._transform_row_wrapper(row)
            row = self._source_reader.get_row()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _transform_row(self, row):
        """
        Transforms the natural keys of dimensions to technical keys. Returns the transformed row with technical keys.

        :param list|dict|() row: The source row.

        :rtype list:
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _load_ignored_rows(self):
        """
        Loads the ignored rows into the database.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _load_parked_rows(self):
        """
        Loads the parked rows into the database.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _load_transformed_rows(self):
        """
        Loads the successfully transformed rows into the database.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _log_statistics(self):
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
    def transform_source_rows(self):
        """
        Transforms the rows for the source system into (partial) dimensional data.
        """
        # Start timer for overall progress.
        self._time0 = time.perf_counter()

        # Transform all source rows.
        with self._source_reader:
            with self._transformed_writer:
                with self._parked_writer:
                    with self._ignored_write:
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
