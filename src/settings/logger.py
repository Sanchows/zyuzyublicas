__all__ = ("configure_logging",)

import dataclasses
import logging

from settings import config


class ColoredFormatter(logging.Formatter):
    @dataclasses.dataclass(frozen=True, slots=True)
    class Color:
        RESET = "\033[0m"
        BLUE = "\033[34m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        RED = "\033[31m"
        MAGENTA = "\033[35m"

    LOG_COLORS = {
        logging.DEBUG: Color.BLUE,
        logging.INFO: Color.GREEN,
        logging.WARNING: Color.YELLOW,
        logging.ERROR: Color.RED,
        logging.CRITICAL: Color.MAGENTA,
    }

    def format(self, record):
        log_color = self.LOG_COLORS.get(record.levelno, self.Color.RESET)
        message = super().format(record)
        return f"{log_color}{message}{self.Color.RESET}"


LOG_FORMAT = "%(asctime)s.%(msecs)03d %(module)15s:%(lineno)5s %(levelname)8s - %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"


def configure_logging() -> None:
    handler = logging.StreamHandler()
    formatter = ColoredFormatter(fmt=LOG_FORMAT, datefmt=DATEFMT)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(config.LOG_LEVEL)
    root_logger.addHandler(handler)
