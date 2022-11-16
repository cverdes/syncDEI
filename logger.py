import logging
from logging.handlers import RotatingFileHandler

class Logger():

    def __init__(self):
        super().__init__()

        log_formatter = logging.Formatter('%(asctime)s %(message)s')
        logFile = "log.txt"

        my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
        my_handler.setFormatter(log_formatter)
        my_handler.setLevel(logging.INFO)

        self.app_log = logging.getLogger('root')
        self.app_log.setLevel(logging.INFO)
        self.app_log.addHandler(my_handler)

    def info(self, msg):
        self.app_log.info(msg)

    def warning(self, msg):
        self.app_log.warning(msg)

    def exception(self, msg):
        self.app_log.exception(msg)
