import logging
import os


class LoggerHandler:

    def __init__(self):
        self.__logger_file_path = r"/home/laksom/Desktop/projekt_IoT/backend"
        self.__logger_file_full_path = os.path.join(self.__logger_file_path, 'basic.log')

        self.__logger_file_mode = 'a'
        self.__init_logger()

    def __init_logger(self):
        if not os.path.exists(self.__logger_file_path):
            os.makedirs(self.__logger_file_path)

        logging.basicConfig(filename=self.__logger_file_full_path,
                            format='%(asctime)s %(message)s',
                            filemode=self.__logger_file_mode)
        self.__logger = logging.getLogger()
        self.__logger.setLevel(logging.INFO)

    def get_logger(self):
        return self.__logger
