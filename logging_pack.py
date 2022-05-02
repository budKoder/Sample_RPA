import logging


def make_logger(name=None):
    """
    create logger instance
    :param name: logger name
    :return: logger instance
    """
    logger=logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter=logging.Formatter('%(asctime)s \t %(message)s',"%Y-%m-%d %H:%M:%S")

    console_handler=logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler=logging.FileHandler(filename="@bot.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.propagate=False

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger=make_logger()