import logging
import os

class Logger:

    GERAL_LOGS = 'geral_logs'
    LOGS_PATH = 'logs/'

    def __init__(self, log_name) -> None:
        os.makedirs(self.LOGS_PATH, exist_ok=True)
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)
        self.__create_handler()

    def __create_handler(self, specific_log = True, geral_log = True) -> None:
        if specific_log:
            file_handler = logging.FileHandler(f'{self.LOGS_PATH}{self.logger.name}.log')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        if geral_log:
            geral_handler = logging.FileHandler(f'{self.LOGS_PATH}{self.GERAL_LOGS}.log')
            geral_handler.setFormatter(formatter)
            self.logger.addHandler(geral_handler)

        command_handler = logging.StreamHandler()
        command_handler.setFormatter(formatter)
        self.logger.addHandler(command_handler)
    
    def get_logger(self) -> logging.Logger:
        return self.logger

