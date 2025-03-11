import os
import sys
import logging


def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers if any
    if logger.hasHandlers():
        logger.handlers.clear()

    # StreamHandler: INFO+ messages to stdout with print-style formatting
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter("%(message)s"))

    # FileHandler: DEBUG+ messages to file with detailed format
    file_handler = logging.FileHandler(
        os.path.join(os.path.dirname(__file__), "dist_clocks.log")
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    )

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
