import os

from common.logger import SnakeGameLogger

logger = SnakeGameLogger()
log = logger.get_logger()
class Utils:
    @staticmethod
    def create_directory(dir_path: str):
        if (not os.path.exists(dir_path)):
            os.makedirs(dir_path)
            log.info(f"Directory {os.path.basename(dir_path)} created")