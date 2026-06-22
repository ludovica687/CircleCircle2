import logging


class Logger:
    def __init__(self, log_file="app.log"):
        self.logger = logging.getLogger("user_logger")    # create logger by Python

        if len(self.logger.handlers) == 0:

            self.logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            file_handler = logging.FileHandler(
                log_file,
                mode="w",
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)

            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


logger = Logger()