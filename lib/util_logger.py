""" Global Logger Module. """
import logging
import os
import sys

from logging.handlers import TimedRotatingFileHandler

LOG_FILE = f"{os.getenv('SITE_NAME', 'my-app')}.log"
FORMAT = logging.Formatter(
    "%(asctime)s:%(name)s:%(levelname)s:%(funcName)s:%(lineno)d:%(message)s")


def console_handler():
    """
    Prints logs to stdout

    :return: stream handler
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(FORMAT)
    return handler


def file_handler():
    """
    Create a file handler which keeps logs on a timed rotation of 10 days.

    :return: file handler
    """
    handler = TimedRotatingFileHandler(LOG_FILE, interval=10, when='D')
    handler.setFormatter(FORMAT)
    return handler


def get_logger(logger_name):
    """
    Entrypoint for instantiation at the application layer.

    example.
        logger = get_logger(__name__)
        # this will output the module name in output if called outside
        # of the module itself.

    :return: Logger
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler())
    # logger.addHandler(file_handler())
    logger.propagate = False
    return logger
