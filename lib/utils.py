import logging


def init_logging(loggername, level=logging.INFO):
    logging.basicConfig(
        format='%(asctime)s-%(levelname)s[%(filename)s:%(lineno)s:%(funcName)s()] %(message)s',
        datefmt='%d-%b-%y %H:%M:%S'
    )
    logger = logging.getLogger(loggername)
    logger.setLevel(level)
    return logger


logger = init_logging(__name__)
