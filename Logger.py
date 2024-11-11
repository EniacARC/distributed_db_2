import logging
import os

# define log constants
LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/loggerServer.log'


class Logger:
    @staticmethod
    def setup_logger():
        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)
        logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
        """
        Set up the logger configuration.
        """
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    def info(msg: str) -> None:
        """
        Log an info message.

        :param msg: The message to log.
        """
        logging.info(msg)

    @staticmethod
    def debug(msg: str) -> None:
        """
        Log a debug message.

        :param msg: The message to log.
        """
        logging.debug(msg)

    @staticmethod
    def warning(msg: str) -> None:
        """
        Log a warning message.

        :param msg: The message to log.
        """
        logging.warning(msg)

    @staticmethod
    def error(msg: str) -> None:
        """
        Log an error message.

        :param msg: The message to log.
        """
        logging.error(msg)

    @staticmethod
    def exception(msg: str) -> None:
        """
        Log an exception message (used in except blocks).

        :param msg: The message to log.
        """
        logging.exception(msg)
