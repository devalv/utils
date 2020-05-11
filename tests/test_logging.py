"""Logging tests."""
import logging
import os
import unittest
import uuid

from dav_utils.logger import Logging


class TestLogging(unittest.TestCase):
    """Logging test cases."""

    @property
    def last_log_line(self):
        """Return last string from temporary log."""
        with open(self._temp_log, 'r') as log_file:
            lines = log_file.readlines()
        return lines[-1]

    @classmethod
    def setUpClass(cls):
        """Test mock objects.

        add FileHandler to logger.
        """
        cls._temp_log = str(uuid.uuid4())[:4] + '.log'
        logger = Logging(log_date_fmt='%H:%M:%S',
                         log_fmt='%(asctime)s.%(msecs)d|%(levelname).1s|%(message)s',
                         log_lvl='DEBUG')
        test_file_handler = logging.FileHandler(cls._temp_log)
        logger.root_logger.addHandler(test_file_handler)
        cls._instance_class_being_tested = logger

    @classmethod
    def tearDownClass(cls) -> None:
        """Remove temporary log."""
        del cls._instance_class_being_tested
        os.remove(cls._temp_log)

    def test_debug_message(self):
        """Debug message in log."""
        message = 'debug'
        self._instance_class_being_tested.debug(message)
        self.assertIn(message, self.last_log_line)

    def test_info_message(self):
        """Info message in log."""
        message = 'info'
        self._instance_class_being_tested.info('info')
        self.assertIn(message, self.last_log_line)

    def test_error_message(self):
        """Error message in log."""
        message = 'error'
        self._instance_class_being_tested.error('error')
        self.assertIn(message, self.last_log_line)

    def test_warning_message(self):
        """Warning message in log."""
        message = 'warning'
        self._instance_class_being_tested.warning('warning')
        self.assertIn(message, self.last_log_line)

    def test_critical_message(self):
        """Critical message in log."""
        message = 'critical'
        self._instance_class_being_tested.critical('critical')
        self.assertIn(message, self.last_log_line)


if __name__ == '__main__':
    unittest.main()
