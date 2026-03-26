import os

from common.utils import Utils
from common.logger import SnakeGameLogger

from log import *
from Config import *
from Message import *
from Basic_game_functions import select_function
import pygame

# Global Variables
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

# Banner
def banner():
    banner_l = 60
    log.info("-" * banner_l)
    log.info(" " * ((banner_l - len(logger.project_name))//2) + logger.project_name)
    log.info("-" * banner_l)

"""
Main Function
"""
log_file = None
try:
    logger = SnakeGameLogger()
    log = logger.get_logger()

    log_dir = os.path.join(ROOT_PATH, "logs")
    Utils.create_directory(log_dir)
    log_file = logger.initialize_log_file(log_dir)

    banner()

except Exception as msg:
    log.error("Unexpected error happened. Terminating the system")
    log.error(f"Error: {msg}")
    exit(1)

finally:
    if (log_file):
        log_file.flush()
        log_file.close()

