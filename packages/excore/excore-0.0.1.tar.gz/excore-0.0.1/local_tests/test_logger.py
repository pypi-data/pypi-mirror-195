from core.logger import logger
from call import t

# logger.info("asdasdasd")

# logger.critical("!!!!")


def test():

    logger.debug("This is debug information")
    logger.info("This is info information")
    logger.warning("This is warn information")
    logger.error("This is error information")
    t()

test()

