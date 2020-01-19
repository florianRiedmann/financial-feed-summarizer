import logging

logger = logging.getLogger()  # create logger
logger.setLevel(logging.INFO)  # set logging level
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")  # create logging format
handler = logging.StreamHandler()  # create stream handler
handler.setFormatter(formatter)  # set streamhandler logging format
logger.addHandler(handler)  # add handler to logger
