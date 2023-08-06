import uuid


class Singleton(object):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        """
        Function to make the log entry class singleton
        :param args: standard arguments
        :param kwargs: dictionary arguments
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
            cls._instances[cls].set_trace_id(str(uuid.uuid4()))
        return cls._instances[cls]


class LogEntry(Singleton):
    """
    Log Entry class used to build the context object
    for standard logging
    """

    def __init__(self):
        self.__generic_context = {}

    def get_execution_id(self):
        return self.__execution_id

    def set_execution_id(self, value: str):
        self.__execution_id = value

    def get_trace_id(self):
        return self.__trace_id

    def set_trace_id(self, value: str):
        self.__trace_id = value

    def get_code_version(self):
        return self.__code_version

    def set_code_version(self, value: str):
        self.__code_version = value

    def get_line_number(self):
        return self.__line_number

    def set_line_number(self, value: str):
        self.__line_number = value

    def get_method_name (self):
        return self.__method_name

    def set_method_name (self, value: str):
        self.__method_name = value

    def get_file_name(self):
        return self.__file_name

    def set_file_name(self, value: str):
        self.__file_name = value

    def get_application_name(self):
        return self.__application_name

    def set_application_name(self, value: str):
        self.__application_name = value

    def set_generic_context(self, key:str, value: object):
        self.__generic_context[key] = value

    def get_generic_context(self):
        return self.__generic_context
