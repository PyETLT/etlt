"""
ETLT

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import re

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
        match = re.match(r'/^([a-z]+):(.*)/', expression)
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
        if not re.match(r'/^([a-z]+)$/', scheme):
            raise ValueError('%s is not a valid scheme' % scheme)

        if scheme in SimpleConditionFactory._constructors:
            raise ValueError('Scheme %s is registered already' % scheme)

        SimpleConditionFactory._constructors[scheme] = constructor

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_condition(field, expression):
        """

        :param str field: The name of the field.
        :param expression: The expression (including scheme).

        :rtype: gdwh.map.SimpleCondition.SimpleCondition
        """
        scheme, actual = SimpleConditionFactory._split_scheme(expression)

        if scheme not in SimpleConditionFactory._constructors:
            raise ValueError('Scheme %s is not registered' % scheme)

        return SimpleConditionFactory._constructors[scheme](field, actual)

# ----------------------------------------------------------------------------------------------------------------------
SimpleConditionFactory.register_scheme('glob', GlobCondition.__init__)
SimpleConditionFactory.register_scheme('plain', PlainCondition.__init__)
SimpleConditionFactory.register_scheme('re', RegularExpressionCondition.__init__)
SimpleConditionFactory.register_scheme('true', TrueCondition.__init__)
