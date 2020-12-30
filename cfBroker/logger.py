import logging
import inspect


def getLogger(appSettings):
    logLevel = appSettings['logging']['level']
    className = str(inspect.stack()[1][0].f_locals["self"].__class__.__name__)
    logger = logging.getLogger(className)
    logger.setLevel(logLevel)

    return logger