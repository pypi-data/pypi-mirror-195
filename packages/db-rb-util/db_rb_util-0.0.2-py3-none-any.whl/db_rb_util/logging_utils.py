"""Module that wraps the logging package."""

import logging
import logging.config
import logging.handlers

# propagate logging levels
CRITICAL = logging.CRITICAL
FATAL = CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

__pdoc__ = {"_setup_logging": True}


def _setup_logging(*, name: str = None, default_level: int = logging.INFO):
    """
    Log configuration for the root logger.

    Args:
        name: get logger
        default_level: default logging level for the logger object, options: INFO, DEBUG, ERROR.

    Returns:
        NO return
    """
    logging.basicConfig(
        level=default_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    logging.captureWarnings(True)
    logger = logging.getLogger(name=name)
    logger.info("Set up logger %s", name)


def get_logger(name: str = None):
    """
    Access the logging.getLogger(Name=None).

    Return a logger with the specified Name, creating it if necessary.
    If no name is specified, return the root logger.

    Attention:
        calling .info and etc immediately after calling get_logger() will not output anything!

    neither the logger or the root logger has been set up, please call setup_logging() before trying
     to log anything.

    Args:
        name: Name of the logger object to be created.

    Returns: logger object
    """
    return logging.getLogger(name)


def init_logging(*, name: str = None, default_level: int = logging.INFO):
    """
    One stop initialization of the logger object.

    In the end, it will initialize the root logger with the specifications defined in the
    logging.yaml and will return a named (name) logger object with extra custom fields specified in
    the logging.yaml
    The return logger object is essentially a logging.logger object.

    Args:
        name: name of the logger object.
        default_level: default logging level

    Returns:
        a logger object
    """
    named_logger = logging.getLogger(name)
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("nose").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("db_logger").setLevel(logging.INFO)
    _setup_logging(name=name, default_level=default_level)
    return named_logger
