# -*- coding: utf-8 -*-
"""Descriptors for extra type checking."""
import functools
import inspect
import os
from uuid import UUID


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


class BoolType(TypeChecker):
    """Descriptor for bool checking."""

    def __init__(self, name):
        """Use 'bool' for TypeChecker value_type."""
        super().__init__(name, bool)


class NullableDictType(DictType):
    """Descriptor for dict checking."""

    def __set__(self, instance, value):
        """Check that attribute value type equals value_type."""
        if isinstance(value, self.value_type) or value is None:
            instance.__dict__[self.name] = value
        else:
            raise TypeError('{val} is not a {val_type}'.format(val=value, val_type=self.value_type))


class NullableStringType(StringType):
    """Descriptor for nullable string checking."""

    def __set__(self, instance, value):
        """Check that attribute value type equals value_type."""
        if isinstance(value, self.value_type) or value is None:
            instance.__dict__[self.name] = value
        else:
            raise TypeError('{val} is not a {val_type}'.format(val=value, val_type=self.value_type))


class NullableIntType(IntType):
    """Descriptor for nullable int checking."""

    def __set__(self, instance, value):
        """Check that attribute value type equals value_type."""
        if isinstance(value, self.value_type) or value is None:
            instance.__dict__[self.name] = value
        else:
            raise TypeError('{val} is not a {val_type}'.format(val=value, val_type=self.value_type))


class UuidStringType(NullableStringType):
    """Check that string is a uuid-representation."""

    def __set__(self, instance, value):
        """Check that attribute value can be converted to UUID."""
        try:
            if value:
                UUID(value)
        except (ValueError, AttributeError):
            raise TypeError('{val} is not a uuid string.'.format(val=value))
        else:
            super().__set__(instance, value)


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


def argument_type_checker(func):
    """Compare function argument type annotations with value types."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arguments = inspect.getfullargspec(func).args
        annotations = func.__annotations__

        if annotations:
            for idx, arg_name in enumerate(arguments):
                arg_annotation = annotations.get(arg_name)
                arg_value = args[idx] if len(args) > idx else None
                if arg_annotation and arg_value and not isinstance(arg_value, arg_annotation):
                    raise TypeError('{arg} is not a proper {arg_type}.'.format(arg=arg_value, arg_type=arg_annotation))

            for kwarg in kwargs:
                kwarg_annotation = annotations.get(kwarg)
                kwarg_value = kwargs[kwarg]
                if kwarg_annotation and kwarg_value and not isinstance(kwarg_value, kwarg_annotation):
                    raise TypeError(
                        '{kwarg} is not a proper {arg_type}.'.format(kwarg=kwarg, arg_type=kwarg_annotation))

        return func(*args, **kwargs)
    return wrapper
