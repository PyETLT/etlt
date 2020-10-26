import re

from etlt.condition.FalseCondition import FalseCondition
from etlt.condition.GlobCondition import GlobCondition
from etlt.condition.PlainCondition import PlainCondition
from etlt.condition.RegularExpressionCondition import RegularExpressionCondition
from etlt.condition.TrueCondition import TrueCondition


class SimpleConditionFactory:
    """
    A factory for simple conditions.
    """
    _constructors = {}
    """
    A map from scheme to object constructors.

    dict[str, callable]
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _split_scheme(expression):
        """
        Splits the scheme and actual expression

        :param str expression: The expression.

        :rtype: str
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
    def register_scheme(scheme, constructor):
        """
        Registers a scheme.

        :param str scheme: The scheme.
        :param callable constructor: The SimpleCondition constructor.
        """
        if not re.search(r'^[a-z]+$', scheme):
            raise ValueError('{0!s} is not a valid scheme'.format(scheme))

        if scheme in SimpleConditionFactory._constructors:
            raise ValueError('Scheme {0!s} is registered already'.format(scheme))

        SimpleConditionFactory._constructors[scheme] = constructor

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_condition(field, expression):
        """

        :param str field: The name of the field.
        :param expression: The expression (including scheme).

        :rtype: gdwh.map.SimpleCondition.SimpleCondition
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
