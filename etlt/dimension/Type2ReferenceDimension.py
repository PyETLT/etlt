import abc
import datetime
from typing import Any, Dict, List, Optional


class Type2ReferenceDimension(metaclass=abc.ABCMeta):
    """
    Abstract class for type2 dimensions for which the reference data is supplied with date intervals.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """

        self._key_key: str = ''
        """
        The key in the dict returned by call_stored_procedure holding the technical ID.
        """

        self._key_date_start: str = ''
        """
        The key in the dict returned by call_stored_procedure holding the start date.
        """

        self._key_date_end: str = ''
        """
        The key in the dict returned by call_stored_procedure holding the end date.
        """

        self._map: Dict[Any, List[Any]] = {}
        """
        The map from natural keys to lists of tuples with start date, end date, and technical keys. The dates must be in
        ISO 8601 (YYYY-MM-DD) format.
        """

        self.pre_load_data()

    # ------------------------------------------------------------------------------------------------------------------
    def get_id(self, natural_key: Any, date: str, enhancement: Any = None) -> Optional[int]:
        """
        Returns the technical ID for a natural key at a date or None if the given natural key is not valid.

        :param natural_key: The natural key.
        :param date: The date in ISO 8601 (YYYY-MM-DD) format.
        :param enhancement: Enhancement data of the dimension row.
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
            self._map[natural_key].append((row[self._key_date_start], row[self._key_date_end], row[self._key_key]))
        else:
            self._map[natural_key].append((date, date, None))

        return row[self._key_key]

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def call_stored_procedure(self, natural_key: Any, date: str, enhancement: Any) -> Dict[str, Any]:
        """
        Call a stored procedure for getting the technical key of a natural key at a date. Returns the technical ID or
        None if the given natural key is not valid.

        :param natural_key: The natural key.
        :param date: The date in ISO 8601 (YYYY-MM-DD) format.
        :param enhancement: Enhancement data of the dimension row.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def pre_load_data(self) -> None:
        """
        Can be overridden to preload lookup data from a dimension table.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def pre_call_stored_procedure(self) -> None:
        """
        This method is invoked before call the stored procedure for getting the technical key of a natural key.

        In a concurrent environment override this method to acquire a lock on the dimension or dimension hierarchy.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def post_call_stored_procedure(self, success: bool) -> None:
        """
        This method is invoked after calling the stored procedure for getting the technical key of a natural key.

        In a concurrent environment override this method to release a lock on the dimension or dimension hierarchy and
        to commit or rollback the transaction.

        :param success: True: the stored procedure is executed successfully. False: an exception has occurred.
        """
        pass

# ----------------------------------------------------------------------------------------------------------------------
