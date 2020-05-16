# -*- coding: utf-8 -*-
"""Some utils for pure python scripts."""

import datetime
import io
import json
import os
from abc import ABC
from types import GeneratorType


class Util(ABC):
    """Some useful utils methods."""

    def update(self, attrs_dict: dict):
        """Update class public attrs."""
        for attr in attrs_dict:
            if attr.startswith('_'):
                continue
            if hasattr(self.__class__, attr) and callable(getattr(self.__class__, attr)):  # noqa
                continue
            self.__setattr__(attr.lower(), attrs_dict[attr])

    @staticmethod
    def check_exists(file_path: str) -> str:
        """Raise FileNotFoundError if file_path not exists."""
        if not os.path.exists(file_path):
            file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_path)  # noqa

        if not os.path.exists(file_path):
            raise FileNotFoundError('File {} not exists.'.format(file_path))

        return file_path

    @staticmethod
    def check_not_exists(file_path: str) -> str:
        """Raise FileExistsError if file_path already exists."""
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
    def date_to_str(date: datetime.datetime, date_fmt: str):
        """Convert date/datetime to str."""
        try:
            converted = datetime.datetime.strftime(date, date_fmt)
        except (TypeError, ValueError) as conversion_error:
            raise ValueError(conversion_error)
        return converted

    @staticmethod
    def read_file_gen(file_name: str):
        """Line by line read the file_name file."""
        assert (isinstance(file_name, str))
        with open(file_name, 'rt') as f:
            for line in f:
                if line:
                    yield line

    @staticmethod
    def save_text_file(file_path: str, txt_data):
        """Save file in plaint text format."""
        with io.open(file_path, mode='w', encoding='utf-8') as output_f:
            if isinstance(txt_data, list) or isinstance(txt_data, GeneratorType):
                output_f.writelines(txt_data)
            else:
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
