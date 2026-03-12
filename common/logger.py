import logging
import sys
import re
import os
from datetime import datetime

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
CUSTOM_LOG_LEVEL = 25 # Custom level between INFO and WARNING
CUSTOM_LOG_LEVEL_NAME = "CUSTOM"
class ColouredFormatter(logging.Formatter):
    __level_colours = {
        "INFO": GREEN,
        "DEBUG": BLUE,
        "WARNING": YELLOW,
        "ERROR": RED,
        "CRITICAL": MAGENTA
    }

    def __init__(self, log_format: str, date_format: str, use_colours = True) -> None:
        super().__init__(log_format, date_format)
        self.__use_colours = use_colours

    def format(self, record: logging.LogRecord) -> str:
        level_name = record.levelname

        if (self.__use_colours and level_name in self.__level_colours):
            record.levelname = '\033[1;%d;%dm' % (30 + WHITE, 40 + self.__level_colours[level_name]) + level_name + '\033[0m'
            record.msg = '\033[0;%dm' % (30 + self.__level_colours[level_name]) + record.msg + '\033[0m'

        return super().format(record)

class PlainFormatter(logging.Formatter):
    def format(self, record):
        # Regex to remove ANSI color codes
        record.levelname = re.sub(r'\033\[([0-9]+)(;[0-9]+)*m', '', record.levelname)
        record.msg = re.sub(r'\033\[([0-9]+)(;[0-9]+)*m', '', record.msg)
        return super().format(record)

class InfoFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return (record.levelno in (logging.INFO, logging.DEBUG))

class DefaultFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return (record.levelno != CUSTOM_LOG_LEVEL)

class CustomFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return (record.levelno == CUSTOM_LOG_LEVEL)

class SnakeGameLogger:
    _logger_instance = None
    logger = None
    log_format = "%(asctime)s | %(module)s | %(funcName)s | %(levelname)s | %(message)s"
    custom_log_format = "%(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    project_name = "Snake Game"
    log_file_name = f"{project_name.lower().replace(' ', '_')}.log"

    def __new__(logger_class):
        if (logger_class._logger_instance is None):
            logger_class._logger_instance = super(SnakeGameLogger, logger_class).__new__(logger_class)
            SnakeGameLogger.logger = logging.getLogger(SnakeGameLogger.project_name)
            SnakeGameLogger.logger.setLevel(logging.INFO)
            logging.addLevelName(CUSTOM_LOG_LEVEL, CUSTOM_LOG_LEVEL_NAME)

            # Console handlers
            console_info_handler = logging.StreamHandler(stream=sys.stdout)
            console_info_handler.setLevel(logging.DEBUG)
            console_info_handler.addFilter(InfoFilter())

            console_warn_handler = logging.StreamHandler(stream=sys.stderr)
            console_warn_handler.setLevel(logging.WARN)
            console_warn_handler.addFilter(DefaultFilter())

            console_custom_handler = logging.StreamHandler(stream=sys.stdout)
            console_custom_handler.setLevel(CUSTOM_LOG_LEVEL)
            console_custom_handler.addFilter(CustomFilter())

            console_formatter = ColouredFormatter(SnakeGameLogger.log_format, SnakeGameLogger.date_format)
            console_info_handler.setFormatter(console_formatter)
            console_warn_handler.setFormatter(console_formatter)

            custom_console_formatter = logging.Formatter(SnakeGameLogger.custom_log_format)
            console_custom_handler.setFormatter(custom_console_formatter)

            SnakeGameLogger.logger.addHandler(console_info_handler)
            SnakeGameLogger.logger.addHandler(console_warn_handler)
            SnakeGameLogger.logger.addHandler(console_custom_handler)

        return logger_class._logger_instance

    def get_logger(self):
        return self.logger

    def custom_log(self, message: str, *args, **kwargs) -> None:
        self.logger.log(CUSTOM_LOG_LEVEL, message, *args, **kwargs)

    def initialize_log_file(self, log_dir):
        log_file_path = os.path.join(log_dir, SnakeGameLogger.log_file_name)

        # Log Rollback
        if (os.path.isfile(log_file_path)):
            time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.rename(log_file_path, f"{log_file_path}_{time_stamp}")

        # File Handler
        file_handler = logging.FileHandler(log_file_path)
        file_handler.addFilter(DefaultFilter())
        file_formatter = PlainFormatter(SnakeGameLogger.log_format)
        file_handler.setFormatter(file_formatter)
        SnakeGameLogger.logger.addHandler(file_handler)

        # Custom Logging File Handler
        custom_file_handler = logging.FileHandler(log_file_path)
        custom_file_handler.addFilter(CustomFilter())
        custom_file_formatter = PlainFormatter(SnakeGameLogger.custom_log_format)
        custom_file_handler.setFormatter(custom_file_formatter)
        SnakeGameLogger.logger.addHandler(custom_file_handler)

        log_file = open(log_file_path, "w+")
        log_file.write("\n")
        log_file.flush()

        return log_file