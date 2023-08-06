import unittest
from src.dna_logger import logger
log = logger.get_instance('test', "INFO", "2.0")
log_entry = log.get_logentry()

class Testing(unittest.TestCase):

    def test_execution_id(self):
        log_entry.set_execution_id('1')
        self.assertEqual( log_entry.get_execution_id(), '1', "Valid execution id response")

    def test_trace_id(self):
        log_entry.set_trace_id('123')
        self.assertEqual( log_entry.get_trace_id(), '123', "Valid trace id response")

    def test_code_version(self):
        self.assertEqual( log_entry.get_code_version(), '2.0', "Valid code version response")

    def test_line_number(self):
        log.info('Test line number')
        self.assertEqual( log_entry.get_line_number(), '20', "Valid line number response")

    def test_method_name(self):
        log.info('Test method name')
        self.assertEqual( log_entry.get_method_name(), 'test_method_name', "Valid method name response")

    def test_file_name(self):
        log.info('Test file name')
        self.assertEqual( log_entry.get_file_name(), 'test_log.py', "Valid file name response")

    def test_application_name(self):
        log.info('Test application name')
        self.assertEqual( log_entry.get_application_name(), 'test', "Valid application name response")

    def test_generic_context(self):
        log_entry.set_generic_context("container", 1)
        self.assertEqual( log_entry.get_generic_context()["container"], 1, "Valid generic context response")

if __name__ == '__main__':
    unittest.main()
