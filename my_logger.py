import logging


class MyLogger:
    def __init__(self):
        self.logger = logging.getLogger('Main')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(filename="./test.log", encoding="utf8")
