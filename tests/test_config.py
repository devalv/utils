"""Config tests."""
import io
import json
import os
import unittest
import uuid


from dav_utils.config import Config


class TestConfig(unittest.TestCase):
    """Config test cases."""

    def setUp(self) -> None:
        """Create unique template_name for each test case."""
        self._template_name = str(uuid.uuid4())[:4] + '.json'

    def tearDown(self) -> None:
        """Remove temporary config file after each test case."""
        os.remove(self._template_name)

    def test_init_with_template(self):
        """Existing config loader test case."""
        json_data = {'test_param_1': -1, 'test_param_2': 0, 'test_param_3': '1'}

        with io.open(self._template_name, mode="w", encoding="utf-8") as json_file:  # noqa
            json.dump(json_data, json_file, sort_keys=True, indent=2, ensure_ascii=False)  # noqa
        cfg = Config(config_file=self._template_name)
        self.assertEqual(-1, cfg.test_param_1)
        self.assertEqual(0, cfg.test_param_2)
        self.assertEqual('1', cfg.test_param_3)
        self.assertTrue(True)

    def test_create_template(self):
        """Config template creator test case."""
        cls = Config()
        cls.create_template(self._template_name)
        self.assertTrue(os.path.exists(self._template_name))

        with open(self._template_name) as config_file:
            config_dict = json.load(config_file)

        self.assertIsInstance(config_dict, dict)
        self.assertIn('LOG_LVL', config_dict)
        self.assertTrue(True)

    def test_load_template(self):
        """Config loader test case."""
        cls = Config()
        cls.create_template(self._template_name)
        self.assertTrue(os.path.exists(self._template_name))

        with open(self._template_name) as config_file:
            file_data = config_file.read()

        file_data = file_data.replace('"%H:%M:%S"', '"%Y-%m-%d %H:%M:%S"')
        with open(self._template_name, 'w') as config_file:
            config_file.write(file_data)

        del cls

        updated_cls = Config(self._template_name)
        self.assertEqual('%Y-%m-%d %H:%M:%S', updated_cls.log_date_fmt)
        updated_cls.log.debug('test')
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
