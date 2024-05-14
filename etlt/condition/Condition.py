import abc
from typing import Any, Dict


class Condition(metaclass=abc.ABCMeta):
    """
    An abstract parent class for conditions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def match(self, row: Dict[str, Any]) -> bool:
        """
        Returns True if the row matches this condition. Returns False otherwise.

        :param row: The row.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
