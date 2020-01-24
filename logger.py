import logging
import sys

from config import LOG_TO_FILE, LOG_FILE_NAME

logger = logging.getLogger()  # create logger
logger.setLevel(logging.INFO)  # set logging level
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")  # create logging format
stream_handler = logging.StreamHandler(sys.stdout)  # create stream handler to stdout
stream_handler.setFormatter(formatter)  # set stream handler logging format
logger.addHandler(stream_handler)  # add handler to logger

if LOG_TO_FILE:
    file_handler = logging.FileHandler(LOG_FILE_NAME)  # create file handler
    file_handler.setFormatter(formatter)  # set file handler logging format
    logger.addHandler(file_handler)  # add file handler to logger
