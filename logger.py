import logging

class Logger():

    def __init__(self):
        super().__init__()
        logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s %(message)s")

    def info(self, msg):
        logging.info(msg)

    def warning(self, msg):
        logging.warning(msg)

    def exception(self, msg):
        logging.exception(msg)
