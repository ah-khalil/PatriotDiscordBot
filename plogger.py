import logging


# @todo Allow custom log level setting, file location and formatting
# @body Currently, the logger uses DEBUG log levels and places all logs
# @body in log.txt. It also has only on format.
def get_p_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.FileHandler(r'log.txt')
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
