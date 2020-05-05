# -*- coding: utf-8 -*-

"""Some useful utils for pure python scripts."""
import datetime
import io
import json
import logging
import os
import sys
from abc import ABC


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
            raise TypeError(f'{self.name}={value} is not a {self.value_type}')

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


class Util(ABC):
    """Some useful utils methods."""

    def update(self, config_dict: dict):
        """Update class public attrs."""
        for attr in config_dict:
            if attr.startswith('_'):
                continue
            if hasattr(self.__class__, attr) and callable(getattr(self.__class__, attr)):  # noqa
                continue
            self.__setattr__(attr.lower(), config_dict[attr])

    @staticmethod
    def check_exists(file_path: str) -> str:
        """Check file_path for exists."""
        if not os.path.exists(file_path):
            file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_path)  # noqa

        if not os.path.exists(file_path):
            raise FileNotFoundError('File {} not exists.'.format(file_path))

        return file_path

    @staticmethod
    def check_not_exists(file_path: str) -> str:
        """Check that there is no file_path."""
        if os.path.exists(file_path):
            raise FileExistsError('File {} already exists.'.format(file_path))
        return file_path

    @staticmethod
    def check_extension(file_name: str, extension_list: frozenset):
        """Compare extension of file_name and extension.

        file_name example: 'config.json'
        extension_list example: ('.json')
        """
        __, file_ext = os.path.splitext(file_name)
        assert file_ext in extension_list

    @staticmethod
    def str_to_date(date_str: str, date_fmt: str):
        """Convert str to date."""
        try:
            converted = datetime.datetime.strptime(date_str, date_fmt).date()
        except (TypeError, ValueError) as conversion_error:
            raise ValueError(conversion_error)
        return converted

    @staticmethod
    def date_to_str(date: datetime.date, date_fmt: str):
        """Convert date to str."""
        try:
            converted = datetime.datetime.strftime(date, date_fmt)
        except (TypeError, ValueError) as conversion_error:
            raise ValueError(conversion_error)
        return converted

    @staticmethod
    def read_file_gen(file_name: str):
        """Line by line read the log file."""
        assert (isinstance(file_name, str))
        with open(file_name, 'rt') as f:
            for line in f:
                if line:
                    yield line

    @staticmethod
    def save_text_file(file_path: str, txt_data):
        """Save file in plaint text format."""
        with io.open(file_path, mode='w', encoding='utf-8') as output_f:
            output_f.write(txt_data)

    @staticmethod
    def save_json_file(file_path: str, json_data):
        """Save file in JSON format."""
        with io.open(file_path, mode="w", encoding="utf-8") as json_file:  # noqa
            json.dump(json_data, json_file, sort_keys=True, indent=2, ensure_ascii=False)  # noqa

    def public_attrs(self) -> dict:
        """Return dictionary of class public attributes and properties."""
        result_dict = dict()
        for attr in dir(self):
            if attr.startswith('_'):
                continue
            if hasattr(self.__class__, attr) and callable(getattr(self.__class__, attr)):  # noqa
                continue
            attr_value = getattr(self.__class__, attr) if hasattr(self.__class__, attr) else self.__getattribute__(attr)  # noqa
            if isinstance(attr_value, property):
                continue
            result_dict[attr] = attr_value
        return result_dict


class Logging:
    """Script logger configuration and methods.

    log_date_fmt: log date format (only str)
    log_fmt: log format (only str)
    log_lvl: log level (logging.DEBUG, logging.INFO and etc.)
    file_handler is missing intentionally. Use OS features.
    """

    log_date_fmt = StringType('log_date_fmt')
    log_fmt = StringType('log_fmt')
    log_lvl = StringType('log_lvl')

    def __init__(self,
                 log_date_fmt: str,
                 log_fmt: str,
                 log_lvl: str):
        """Initialize script logger.

        log_date_fmt: log date format (only str)
        log_fmt: log format (only str)
        log_lvl: log level (logging.DEBUG, logging.INFO and etc.)
        """
        self.root_logger = logging.getLogger(__name__)
        self.log_lvl = log_lvl
        self.root_logger.setLevel(self.log_lvl)
        self.root_logger.propagate = 0
        self.log_fmt = log_fmt
        self.log_date_fmt = log_date_fmt
        formatter = logging.Formatter(fmt=self.log_fmt, datefmt=self.log_date_fmt)
        self.add_stdout_handler(formatter)
        self.debug('Log configuration applied.')

    @property
    def log_lvl(self):
        """Return logging.log_level."""
        return self.__log_lvl

    @log_lvl.setter
    def log_lvl(self, level: str):
        """Check that level is one of logging.logging_levels."""
        _logging_levels = {
            'CRITICAL': logging.CRITICAL,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG
        }

        level = _logging_levels.get(level.upper(), logging.ERROR)
        self.__log_lvl = logging.getLevelName(level)

    def add_stdout_handler(self, formatter):
        """Add stdout handler for root_logger."""
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)
        self.root_logger.addHandler(handler)

    def debug(self, message: str):
        """Write debug message to root_logger."""
        self.root_logger.debug(message)

    def info(self, message: str):
        """Write info message to root_logger."""
        self.root_logger.info(message)

    def warning(self, message: str):
        """Write warning message to root_logger."""
        self.root_logger.warning(message)

    def error(self, message: str):
        """Write error message to root_logger."""
        self.root_logger.error(message)

    def critical(self, message: str):
        """Write critical message to root_logger."""
        self.root_logger.critical(message)

    def __del__(self):
        """Want to delete all handlers created by Logger."""
        self.root_logger.debug('Remove existing handlers.')
        for handler in self.root_logger.handlers.copy():
            handler.close()
            self.root_logger.removeHandler(handler)


class Config(Util):
    """Script configuration.

    logging parameters:
        log_date_fmt: log date format (only str)
        log_fmt: log format (only str)
        log_lvl: log level (logging.DEBUG, logging.INFO and etc.)

    __extensions: acceptable configuration file extensions
    """

    __extensions = frozenset(['.json'])
    log_date_fmt = StringType('log_date_fmt')
    log_fmt = StringType('log_fmt')
    log_lvl = StringType('log_lvl')

    def __init__(self, config_file: str = None):
        """Load configuration parameters from config_file."""
        self.log_date_fmt = '%H:%M:%S'
        self.log_fmt = '%(asctime)s.%(msecs)d|%(levelname).1s|%(message)s'
        self.log_lvl = 'DEBUG'

        if config_file:
            file_config = self.load(config_file)
            self.update(file_config)

        self.__logger = Logging(self.log_date_fmt, self.log_fmt, self.log_lvl)

    @property
    def log(self):
        """Script logger instance."""
        return self.__logger

    def load(self, config_file: str):
        """Load configuration attributes from a config_file."""
        config_file = self.check_exists(config_file)
        self.check_extension(config_file, self.__extensions)

        with io.open(config_file, mode='r', encoding='utf-8') as json_config:
            file_config = json.load(json_config)

        return file_config

    def create_template(self, file_path):
        """Create config file template."""
        # For extra verbosity keys should be in upper register
        attrs = {k.upper(): v for k, v in self.public_attrs().items()}
        self.save_json_file(file_path, attrs)
        self.log.info(f'Template {file_path} created.')
