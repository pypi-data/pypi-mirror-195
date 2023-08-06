import json
import logging
import logging.config
import traceback
from dna_logger import logmodel
from datetime import datetime
import inspect

log_levels = ['INFO', 'DEBUG', 'ERROR', 'WARNING', 'FATAL']

def get_instance(name: str, level="INFO", code_version="1.0"):
    """
    Function to get a instance of logger
    Default log level is INFO
    :param name: class name
    :param level: log level
    :param code_version: code version
    :return: logger instance
    """
    if level not in log_levels:
        raise Exception(f'Invalid log level found: {level}')
    logger = Logger(name, level)
    logentry = logger.get_logentry()
    logentry.set_code_version(code_version)
    return logger


class Logger:

    def __init__(self, name: str, level: str):
        self.__name = name
        self.__logger = self.__create_logger(level)
        self.__logentry = logmodel.LogEntry()
        self.__logentry.set_application_name(name)

    def __create_logger(self, level):
        """
        Function to config the logger
        :param level: log level
        :return: logger configuration
        """
        default_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                }
            },
            "handlers": {
                "console": {
                    "formatter": "standard",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout"
                }
            },
            "loggers": {
                "": {
                    "level": level,
                    "handlers": ["console"]
                }
            }
        }
        logging.config.dictConfig(default_config)
        return logging.getLogger(self.__name)

    def get_logentry(self):
        """
        Function to return the singleton log entry object
        :return: logger instance
        """
        return self.__logentry

    def info(self, message: object):
        self.__logger.info(self.__build_message(str(message), 'INFO'))

    def debug(self, message: object):
        self.__logger.debug(self.__build_message(str(message), 'DEBUG'))

    def error(self, message: object):
        self.__logger.error(self.__build_message(str(message), 'ERROR'))

    def error(self, message: object, exception: Exception = None):
        self.__logger.error(self.__build_message(str(message), 'ERROR', exception))

    def warn(self, message: object):
        self.__logger.warning(self.__build_message(str(message), 'WARNING'))

    def fatal(self, message: object):
        self.__logger.fatal(self.__build_message(str(message), 'FATAL'))

    def __build_message(self, message: str, level: str, error: Exception = None):
        """
        Function to build standard Json response for logging
        :param message: log message
        :param level: log level
        :param error: exception
        :return: standard json log
        """
        self.__set_general_log_entry()
        log_message = {}
        context = {}
        exception = {}
        log_message['timestamp'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] +'Z'
        log_message['level'] = level
        log_message['message'] = message
        if error:
            log_message['exception'] = exception
            exception['message'] = str(error)
            exception['type'] = type(error).__name__
            exception['stackTrace'] = traceback.format_exc()
        log_message['context'] = context

        """
        Converting the Class to dict and reading
        the valid keys in the log entry and changing to camelcase.
        """
        log_entry = json.loads(json.dumps(dict(self.__logentry.__dict__)))
        for key in log_entry:
            new_key = key.replace("_LogEntry__", "")
            new_key = new_key.split('_')[0] + ''.join(map(lambda s: s.strip().capitalize(), new_key.split('_')[1::]))
            if new_key == 'genericContext':
                for context_key in log_entry[key]:
                    context[context_key] = log_entry[key][context_key]
            else:
                context[new_key] = log_entry[key]
        return json.dumps(log_message)

    def __set_general_log_entry(self):
        """
        Function to set general log entry
        0th frame will be giving details about __set_general_log_entry
        1st frame will be giving details about __build_message
        2nd frame will be giving details about the function calling __build_message
        3rd frame will be giving the exact details about the logger used in the file
        """
        file_name = str(inspect.getouterframes(inspect.currentframe(), 1)[3][1]).split("/")[-1]
        line_no = str(inspect.getouterframes(inspect.currentframe(), 1)[3][2])
        method_name = str(inspect.getouterframes(inspect.currentframe(), 1)[3][3])
        self.__logentry.set_file_name(file_name)
        self.__logentry.set_method_name(method_name)
        self.__logentry.set_line_number(line_no)

