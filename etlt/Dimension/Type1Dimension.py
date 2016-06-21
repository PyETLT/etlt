"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import abc


# ----------------------------------------------------------------------------------------------------------------------
class Type1Dimension:
    """
    Abstract parent class for translating natural key to a technical key of a type 1 dimension.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """

        self._map = {}
        """
        The map from natural keys to a technical keys.

        :type dict[T, int|None]:
        """

        # Pre-load look up data in to the map.
        self.pre_load_data()

    # ------------------------------------------------------------------------------------------------------------------
    def get_id(self, natural_key, enhancement=None):
        """
        Returns the technical ID for a natural key or None if the given natural key is not valid.

        :param T natural_key: The natural key.
        :param T enhancement: Enhancement data of the dimension row.

        :rtype: int|None
        """
        # If the natural key is known return the technical ID immediately.
        if natural_key in self._map:
            return self._map[natural_key]

        # The natural key is not in the map of this dimension. Call a stored procedure for translating the natural key
        # to a technical key.
        self.acquire_lock()
        try:
            key = self.call_stored_procedure(natural_key, enhancement)
        finally:
            self.release_lock()

        # Add the translation for natural key to technical ID to the map.
        self._map[natural_key] = key

        return key

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def call_stored_procedure(self, natural_key, enhancement):
        """
        Call a stored procedure for getting the technical key for a natural key. Returns the technical ID or None if
        the given natural key is not valid.

        :param T natural_key: The natural key.
        :param T enhancement: Enhancement data of the dimension row.

        :rtype: int|None
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
    def acquire_lock(self):
        """
        In a concurrent environment override this method to acquire a lock on the dimension of dimension hierarchy.

        :rtype: None
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def release_lock(self):
        """
        In a concurrent environment override this method to release a lock on the dimension of dimension hierarchy.

        :rtype: None
        """
        pass

# ----------------------------------------------------------------------------------------------------------------------
