import logging
import sys

logger = logging.getLogger()  # create logger
logger.setLevel(logging.INFO)  # set logging level
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")  # create logging format
handler = logging.StreamHandler(sys.stdout)  # create stream handler to stdout
handler.setFormatter(formatter)  # set streamhandler logging format
logger.addHandler(handler)  # add handler to logger
