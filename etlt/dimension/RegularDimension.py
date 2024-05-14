import abc
from typing import Any, Dict, Optional


class RegularDimension(metaclass=abc.ABCMeta):
    """
    Abstract parent class for translating natural key to a technical key of a regular dimension.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """

        self._map: Dict[Any, Optional[int]] = {}
        """
        The map from natural keys to a technical keys.
        """

        self.pre_load_data()

    # ------------------------------------------------------------------------------------------------------------------
    def get_id(self, natural_key: Any, enhancement: Any = None) -> Optional[int]:
        """
        Returns the technical ID for a natural key or None if the given natural key is not valid.

        :param natural_key: The natural key.
        :param enhancement: Enhancement data of the dimension row.
        """
        # If the natural key is known return the technical ID immediately.
        if natural_key in self._map:
            return self._map[natural_key]

        # The natural key is not in the map of this dimension. Call a stored procedure for translating the natural key
        # to a technical key.
        self.pre_call_stored_procedure()
        success = False
        try:
            key = self.call_stored_procedure(natural_key, enhancement)
            success = True
        finally:
            self.post_call_stored_procedure(success)

        # Add the translation for natural key to technical ID to the map.
        self._map[natural_key] = key

        return key

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def call_stored_procedure(self, natural_key: Any, enhancement: Any) -> Optional[int]:
        """
        Calls a stored procedure for getting the technical key of a natural key. Returns the technical ID or None if
        the given natural key is not valid.

        :param natural_key: The natural key.
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
