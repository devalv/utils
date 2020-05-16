# -*- coding: utf-8 -*-
"""Descriptors for extra type checking."""
import os


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


class WritableFile(StringType):
    """Check that file (value) is a writable file or can be created."""

    def __set__(self, instance, value):
        """Check that file is a file or can be created or has write permissions."""
        super().__set__(instance, value)
        try:
            if os.path.exists(value):
                if os.path.isfile(value):
                    if not os.access(value, os.W_OK):
                        raise PermissionError('{val} can not be edited. Check FS permissions.'.format(val=value))
                else:
                    raise TypeError('{val} is not a file.'.format(val=value))
            file_dir = os.path.dirname(value)
            if not file_dir:
                file_dir = '.'
            if not os.access(file_dir, os.W_OK):
                raise PermissionError('{val} can not be created. Check FS permissions.'.format(val=value))
        except PermissionError as err:
            instance.__dict__[self.name] = None
            raise PermissionError(err)


class HttpMethod(StringType):
    """Check that value is one of http methods."""

    http_methods = frozenset(['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'PATCH', 'OPTIONS'])

    def __set__(self, instance, value):
        """Check that value in allowed http methods."""
        super().__set__(instance, value)
        if value.upper() not in self.http_methods:
            instance.__dict__[self.name] = None
            raise TypeError('{val} is not a HTTP Method.'.format(val=value))
