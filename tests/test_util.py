"""Util and TypeChecker descriptors tests."""
import datetime
import os
import unittest
import uuid
from collections.abc import Iterable

from dav_utils.descriptors import (BoolType, DictType, HttpMethod, IntType, ListType,
                                   NullableDictType, NullableIntType, NullableStringType, StringType,
                                   UuidStringType, WritableFile, argument_type_checker)
from dav_utils.utils import Util


class TestUtil(unittest.TestCase):
    """Util methods tests."""

    @classmethod
    def setUpClass(cls):
        """Test mock values."""

        class Test(Util):

            def method(self, val):
                pass

        cls._instance_class_being_tested = Test()
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
        cls.update({'_private_attr': 'updated', 'public_attr': 'updated', 'method': 'method'})
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

    def test_save_text_file_one_line(self):
        """Text file saver test case."""
        cls = self._instance_class_being_tested
        file_path = __file__ + self._temp_value
        cls.save_text_file(file_path, self._temp_value)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)
        self.assertTrue(True)

    def test_save_text_file_multi_line(self):
        """Test file saver with multi line value."""
        cls = self._instance_class_being_tested
        file_path = __file__ + self._temp_value
        random_list = [str(i) + self._temp_value + '\n' for i in range(10)]
        cls.save_text_file(file_path, random_list)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)
        self.assertTrue(True)

    def test_save_text_file_gen(self):
        """Test file saver with generator as data."""
        cls = self._instance_class_being_tested
        file_path = __file__ + self._temp_value
        random_gen = (str(i) + self._temp_value + '\n' for i in range(10))
        cls.save_text_file(file_path, random_gen)
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
            str_type = StringType('str_type')
            nullable_str_type = NullableStringType('nullable_str_type')
            int_type = IntType('int_type')
            nullable_int_type = NullableIntType('nullable_int_type')
            dict_type = DictType('dict_type')
            nullable_dict_type = NullableDictType('nullable_dict_type')
            list_type = ListType('list_type')
            http_method = HttpMethod('http_method')
            writable_file = WritableFile('writable_file')
            bool_type = BoolType('bool_type')
            uuid_string_type = UuidStringType('uuid_string_type')

            @argument_type_checker
            def annotated(self, val: str = None):
                pass

        cls._instance_class_being_tested = TemporaryClass()

    def test_method_annotated_argument(self):
        """Decorator argument_type_checker."""
        try:
            self._instance_class_being_tested.annotated(val='1')
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.annotated('1')
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.annotated(val=1)
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        try:
            self._instance_class_being_tested.annotated(1)
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_dict_type(self):
        """Descriptor DictType descriptor test cases."""
        try:
            self._instance_class_being_tested.dict_type = {'k': 'v'}
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.dict_type = list()
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_nullable_dict_type(self):
        """Descriptor NullableDictType descriptor test cases."""
        try:
            self._instance_class_being_tested.nullable_dict_type = {'k': 'v'}
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.nullable_dict_type = list()
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        try:
            self._instance_class_being_tested.nullable_dict_type = None
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_list_type(self):
        """Descriptor ListType descriptor test cases."""
        try:
            self._instance_class_being_tested.list_type = ['a', 'b']
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.list_type = {'k': 'v'}
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_uuid_string_type(self):
        """Descriptor UuidStringType descriptor test cases."""
        try:
            self._instance_class_being_tested.uuid_string_type = 'ac158335-a0e2-4e59-b722-08328b2985d4'
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.uuid_string_type = 1
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_string_type(self):
        """Descriptor StringType descriptor test cases."""
        try:
            self._instance_class_being_tested.str_type = 'test'
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.str_type = 1
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_nullable_string_type(self):
        """Descriptor NullableStringType descriptor test cases."""
        try:
            self._instance_class_being_tested.nullable_str_type = 'test'
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.nullable_str_type = 1
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        try:
            self._instance_class_being_tested.nullable_str_type = None
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_int_type(self):
        """Descriptor IntType test cases."""
        try:
            self._instance_class_being_tested.int_type = 1
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.int_type = '1'
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_bool_type(self):
        """Descriptor BoolType test cases."""
        try:
            self._instance_class_being_tested.bool_type = True
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.bool_type = '1'
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_nullable_int_type(self):
        """Descriptor NullableIntType test cases."""
        try:
            self._instance_class_being_tested.nullable_int_type = 1
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.nullable_int_type = '1'
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        try:
            self._instance_class_being_tested.nullable_int_type = None
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_writable_file(self):
        """Descriptor WritableFile test cases."""
        # create temporary file
        file_path = __file__ + 'qwe'
        Util().save_text_file(file_path, 'self._temp_value')
        # create temporary dir
        dir_path = 'tmp_dir'
        os.mkdir(dir_path)

        try:
            # permissions should be ok
            self._instance_class_being_tested.writable_file = file_path
        except PermissionError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

        try:
            # permission error
            # change file permissions
            os.chmod(file_path, 0o444)
            self._instance_class_being_tested.writable_file = file_path
        except PermissionError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            # type error
            self._instance_class_being_tested.writable_file = dir_path
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        # change dir permissions
        os.chmod(dir_path, 0o444)

        try:
            # change file permissions
            bad_perm_file_path = os.path.join('.', dir_path, 'qwe')
            self._instance_class_being_tested.writable_file = bad_perm_file_path
        except PermissionError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        # check file without dir
        no_dir_file_path = 'tmp.txt'
        Util().save_text_file(no_dir_file_path, 'self._temp_value')
        try:
            # permissions should be ok
            self._instance_class_being_tested.writable_file = no_dir_file_path
        except PermissionError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

        os.remove(file_path)
        os.remove(no_dir_file_path)
        os.rmdir(dir_path)

    def test_http_method(self):
        """Descriptor HttpMethod test cases."""
        try:
            for method in HttpMethod.http_methods:
                self._instance_class_being_tested.http_method = method
        except TypeError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
        try:
            self._instance_class_being_tested.http_method = 'BAD'
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
