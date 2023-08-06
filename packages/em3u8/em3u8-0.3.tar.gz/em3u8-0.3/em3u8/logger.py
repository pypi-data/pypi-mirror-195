from loguru import logger
import sys

class Log():
    def __init__(self,debug=False):
        if  debug:
            logger.remove()
            logger.add(sys.stdout,level="DEBUG")
            logger.add("em3u8.log",level="DEBUG",rotation="1GB",retention="7 days")
        else:
            logger.remove()
            logger.add(sys.stdout,level="INFO")
            logger.add("em3u8.log",level="INFO",rotation="1GB",retention="7 days")
