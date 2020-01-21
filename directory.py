import os
from logger import logger


def make_directory(*args):
    for elem in args:
        try:
            os.mkdir(elem)
            logger.info(f"INFO: {elem} has been created")
        except FileExistsError:
            logger.info(f"ATTENTION: {elem} already existed")
