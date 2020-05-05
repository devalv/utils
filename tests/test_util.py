"""Util and TypeChecker descriptors tests."""
import datetime
import os
import unittest
import uuid
from collections.abc import Iterable

from utils import IntType, StringType, Util


class TestUtil(unittest.TestCase):
    """Util methods tests."""

    @classmethod
    def setUpClass(cls):
        """Test mock values."""
        cls._instance_class_being_tested = Util()
        cls._temp_value = str(uuid.uuid4())[:4]
        cls._date_fmt = '%Y%m%d'
        cls._valid_date_str = '20200418'
        cls._invalid_date_str = '2020-04-18'
        cls._valid_date = datetime.datetime.now().date()

    def test_public_attrs(self):
        """Class public.attr test case."""
        cls = self._instance_class_being_tested
        cls.test_attr = 'test_attr_value'
        result = cls.public_attrs()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn('test_attr', result)
        self.assertEqual('test_attr_value', result['test_attr'])
        del cls.test_attr
        result = cls.public_attrs()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertNotIn('test_attr', result)

    def test_update(self):
        """Class public.attr updater test case."""
        cls = self._instance_class_being_tested
        cls._private_attr = 'private_value'
        cls.public_attr = 'public_value'
        cls.update({'_private_attr': 'updated', 'public_attr': 'updated'})
        self.assertEqual(cls._private_attr, 'private_value')
        self.assertEqual(cls.public_attr, 'updated')

    def test_check_exists(self):
        """File exists checker test case.."""
        cls = self._instance_class_being_tested
        result = cls.check_exists(__file__)
        self.assertEqual(result, __file__)
        tmp_file_path = __file__ + self._temp_value
        try:
            cls.check_exists(tmp_file_path)
        except FileNotFoundError:
            self.assertTrue(True)
        else:
            self.assertFalse(True)

    def test_check_not_exists(self):
        """File NotExists checker test case.."""
        cls = self._instance_class_being_tested
        file_path = __file__ + self._temp_value
        result = cls.check_not_exists(file_path)
        self.assertEqual(result, file_path)
        try:
            cls.check_not_exists(__file__)
        except FileExistsError:
            self.assertTrue(True)
        else:
            self.assertFalse(False)

    def test_check_extension(self):
        """File extension checker test case."""
        cls = self._instance_class_being_tested
        ext = '.' + __file__.split('.')[-1]

        try:
            cls.check_extension(__file__, ext)
        except AssertionError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

        try:
            cls.check_extension(__file__, self._temp_value)
        except AssertionError:
            self.assertTrue(True)
        else:
            self.assertFalse(True)

    def test_str_to_date(self):
        """Str to date converter test case."""
        cls = self._instance_class_being_tested

        try:
            cls.str_to_date(self._valid_date_str, self._date_fmt)
        except ValueError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

        try:
            cls.str_to_date(self._invalid_date_str, self._date_fmt)
        except ValueError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_date_to_str(self):
        """Date to str converter test case."""
        cls = self._instance_class_being_tested
        try:
            cls.date_to_str(self._valid_date, self._date_fmt)
        except ValueError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

        try:
            cls.date_to_str(self._invalid_date_str, self._date_fmt)
        except ValueError:
            self.assertTrue(True)
        else:
            self.assertFalse(True)

    def test_read_file_gen(self):
        """Read file generator test case."""
        cls = self._instance_class_being_tested
        result = cls.read_file_gen(__file__)
        self.assertIsInstance(result, Iterable)
        self.assertIsInstance(next(result), str)  # noqa

    def test_save_text_file(self):
        """Text file saver test case."""
        cls = self._instance_class_being_tested
        file_path = __file__ + self._temp_value
        cls.save_text_file(file_path, self._temp_value)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)
        self.assertTrue(True)

    def test_save_json_file(self):
        """Json file saver test case."""
        cls = self._instance_class_being_tested
        file_path = __file__ + self._temp_value
        cls.save_json_file(file_path, {'q': 'qwe', 'b': 'bcx'})
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)
        self.assertTrue(True)


class TestDescriptors(unittest.TestCase):
    """Descriptors test cases."""

    @classmethod
    def setUpClass(cls):
        """Test mock values."""
        class TemporaryClass:
            good_str = StringType('good_str')
            bad_str = StringType('bad_str')
            good_int = IntType('good_int')
            bad_int = IntType('bad_int')

            def __init__(self, good_str, bad_str, good_int, bad_int):
                self.good_str = good_str
                self.bad_str = bad_str
                self.good_int = good_int
                self.bad_int = bad_int

        cls._instance_class_being_tested = TemporaryClass('good', 'bad', 5, 0)

    def test_string_type(self):
        """Descriptor StringType descriptor test cases."""
        try:
            self._instance_class_being_tested.good_str = 'test'
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.bad_str = 1
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_int_type(self):
        """Descriptor IntType test cases."""
        try:
            self._instance_class_being_tested.good_int = 1
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.bad_int = '1'
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
