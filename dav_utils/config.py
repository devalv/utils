# -*- coding: utf-8 -*
"""Extendable config template."""

import io
import json

from .descriptors import StringType
from .logger import Logging
from .utils import Util


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

    def create_template(self, file_path: str):
        """Create JSON config file template."""
        # For extra verbosity keys should be in upper register
        attrs = {k.upper(): v for k, v in self.public_attrs().items()}
        self.save_json_file(file_path, attrs)
        self.log.info('Template {file_path} created.'.format(file_path=file_path))
