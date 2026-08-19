import logging
import sys


def setup_logger():

    logger = logging.getLogger()

    if logger.handlers:
        return logger

    logger.setLevel(
        logging.INFO
    )

    handler = logging.StreamHandler(
        sys.stdout
    )

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    )

    handler.setFormatter(
        formatter
    )

    logger.addHandler(
        handler
    )

    return logger


setup_logger()


logger = logging.getLogger(
    "PF_AI"
)