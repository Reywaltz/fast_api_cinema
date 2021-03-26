import logging
import os

class Logger:
    def new_logger(name: str):
        file_logger = logging.getLogger(name)
        file_logger.setLevel(logging.DEBUG)
        if not os.path.exists(os.path.join(os.getcwd(), 'logs')):
            os.mkdir('logs')
        fl = logging.FileHandler(f"logs/{name}.log", encoding='UTF-8')
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fl.setFormatter(formatter)
        file_logger.addHandler(fl)

        return file_logger