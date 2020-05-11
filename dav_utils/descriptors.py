# -*- coding: utf-8 -*-
"""Descriptors for extra type checking."""


class TypeChecker:
    """Descriptor for type checking."""

    def __init__(self, name, value_type):
        """Set attribute name and checking value type."""
        self.name = name
        self.value_type = value_type

    def __set__(self, instance, value):
        """Check that attribute value type equals value_type."""
        if isinstance(value, self.value_type):
            instance.__dict__[self.name] = value
        else:
            raise TypeError('{val} is not a {val_type}'.format(val=value, val_type=self.value_type))

    def __get__(self, instance, class_):
        """Return attribute value."""
        return instance.__dict__[self.name]


class StringType(TypeChecker):
    """Descriptor for string checking."""

    def __init__(self, name):
        """Use 'str' for TypeChecker value_type."""
        super().__init__(name, str)


class IntType(TypeChecker):
    """Descriptor for int checking."""

    def __init__(self, name):
        """Use 'int' for TypeChecker value_type."""
        super().__init__(name, int)


class ListType(TypeChecker):
    """Descriptor for list checking."""

    def __init__(self, name):
        """Use 'list' for TypeChecker value_type."""
        super().__init__(name, list)


class DictType(TypeChecker):
    """Descriptor for dict checking."""

    def __init__(self, name):
        """Use 'dict' for TypeChecker value_type."""
        super().__init__(name, dict)
