# -*- coding: utf-8 -*-
"""stdout Logging template."""

import logging
import sys

from .descriptors import StringType


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
