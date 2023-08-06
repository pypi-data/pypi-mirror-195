import logging
import os
from logging.handlers import TimedRotatingFileHandler


def get_logger():
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] [%(threadName)s] %(message)s"
    )

    file_name = "seek-automation"
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)
    file_handler = TimedRotatingFileHandler(
        os.path.join(os.getcwd(), f"{file_name}.log"),
        when="midnight",
        backupCount=10,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = get_logger()
