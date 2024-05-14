import re
from typing import Callable, Dict, Tuple

from etlt.condition.FalseCondition import FalseCondition
from etlt.condition.GlobCondition import GlobCondition
from etlt.condition.PlainCondition import PlainCondition
from etlt.condition.RegularExpressionCondition import RegularExpressionCondition
from etlt.condition.SimpleCondition import SimpleCondition
from etlt.condition.TrueCondition import TrueCondition


class SimpleConditionFactory:
    """
    A factory for simple conditions.
    """
    _constructors: Dict[str, Callable] = {}
    """
    A map from scheme to object constructors.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _split_scheme(expression: str) -> Tuple[str, str]:
        """
        Splits the scheme and actual expression

        :param expression: The expression.
        """
        match = re.search(r'^([a-z]+):(.*)$', expression)
        if not match:
            scheme = 'plain'
            actual = expression
        else:
            scheme = match.group(1)
            actual = match.group(2)

        return scheme, actual

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def register_scheme(scheme: str, constructor: Callable) -> None:
        """
        Registers a scheme.

        :param scheme: The scheme.
        :param constructor: The SimpleCondition constructor.
        """
        if not re.search(r'^[a-z]+$', scheme):
            raise ValueError('{0!s} is not a valid scheme'.format(scheme))

        if scheme in SimpleConditionFactory._constructors:
            raise ValueError('Scheme {0!s} is registered already'.format(scheme))

        SimpleConditionFactory._constructors[scheme] = constructor

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_condition(field: str, expression: str) -> SimpleCondition:
        """

        :param str field: The name of the field.
        :param expression: The expression (including scheme).
        """
        scheme, expression = SimpleConditionFactory._split_scheme(expression)

        if scheme not in SimpleConditionFactory._constructors:
            raise ValueError('Scheme {0!s} is not registered'.format(scheme))

        return SimpleConditionFactory._constructors[scheme](field, expression)


# ----------------------------------------------------------------------------------------------------------------------
SimpleConditionFactory.register_scheme('false', FalseCondition)
SimpleConditionFactory.register_scheme('glob', GlobCondition)
SimpleConditionFactory.register_scheme('plain', PlainCondition)
SimpleConditionFactory.register_scheme('re', RegularExpressionCondition)
SimpleConditionFactory.register_scheme('true', TrueCondition)
