import abc
import datetime


class Type2ReferenceDimension(metaclass=abc.ABCMeta):
    """
    Abstract class for type2 dimensions for which the reference data is supplied with date intervals.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """

        self._key_key = ''
        """
        The key in the dict returned by call_stored_procedure holding the technical ID.

        :type: str
        """

        self._key_date_start = ''
        """
        The key in the dict returned by call_stored_procedure holding the start date.

        :type: str
        """

        self._key_date_end = ''
        """
        The key in the dict returned by call_stored_procedure holding the end date.

        :type: str
        """

        self._map = {}
        """
        The map from natural keys to lists of tuples with start date, end date, and technical keys. The dates must be in
        ISO 8601 (YYYY-MM-DD) format.

        :type: dict[T, list[(str,str,int|None)]]
        """

        # Pre-load look up data in to the map.
        self.pre_load_data()

    # ------------------------------------------------------------------------------------------------------------------
    def get_id(self, natural_key, date, enhancement=None):
        """
        Returns the technical ID for a natural key at a date or None if the given natural key is not valid.

        :param T natural_key: The natural key.
        :param str date: The date in ISO 8601 (YYYY-MM-DD) format.
        :param T enhancement: Enhancement data of the dimension row.

        :rtype: int|None
        """
        if not date:
            return None

        # If the natural key is known return the technical ID immediately.
        if natural_key in self._map:
            for row in self._map[natural_key]:
                if row[0] <= date <= row[1]:
                    return row[2]

        # The natural key is not in the map of this dimension. Call a stored procedure for translating the natural key
        # to a technical key.
        self.pre_call_stored_procedure()
        success = False
        try:
            row = self.call_stored_procedure(natural_key, date, enhancement)
            # Convert dates to strings in ISO 8601 format.
            if isinstance(row[self._key_date_start], datetime.date):
                row[self._key_date_start] = row[self._key_date_start].isoformat()
            if isinstance(row[self._key_date_end], datetime.date):
                row[self._key_date_end] = row[self._key_date_end].isoformat()
            success = True
        finally:
            self.post_call_stored_procedure(success)

        # Make sure the natural key is in the map.
        if natural_key not in self._map:
            self._map[natural_key] = []

        if row[self._key_key]:
            self._map[natural_key].append((row[self._key_date_start],
                                           row[self._key_date_end],
                                           row[self._key_key]))
        else:
            self._map[natural_key].append((date, date, None))

        return row[self._key_key]

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def call_stored_procedure(self, natural_key, date, enhancement):
        """
        Call a stored procedure for getting the technical key of a natural key at a date. Returns the technical ID or
        None if the given natural key is not valid.

        :param T natural_key: The natural key.
        :param str date: The date in ISO 8601 (YYYY-MM-DD) format.
        :param T enhancement: Enhancement data of the dimension row.

        :rtype: dict
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def pre_load_data(self):
        """
        Can be overridden to pre-load lookup data from a dimension table.

        :rtype: None
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def pre_call_stored_procedure(self):
        """
        This method is invoked before call the stored procedure for getting the technical key of a natural key.

        In a concurrent environment override this method to acquire a lock on the dimension or dimension hierarchy.

        :rtype: None
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def post_call_stored_procedure(self, success):
        """
        This method is invoked after calling the stored procedure for getting the technical key of a natural key.

        In a concurrent environment override this method to release a lock on the dimension or dimension hierarchy and
        to commit or rollback the transaction.

        :param bool success: True: the stored procedure is executed successfully. False: an exception has occurred.

        :rtype: None
        """
        pass

# ----------------------------------------------------------------------------------------------------------------------
