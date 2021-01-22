import logging
import traceback

class OneLogger(logging.getLoggerClass()):
    def __init__(self, logger_name, screen=True, log_path=None, level_str='info'):
        super().__init__(logger_name)
        self.setLevel(level_str)
        self.log_path = log_path
        self.formatter = logging.Formatter(
            '%(asctime)s@' + logger_name + '[%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        if screen:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(self.formatter)
            self.addHandler(stream_handler)

        if self.log_path:
            self.set_logfile(self.log_path)

    def error(self, msg):
        super().error(msg)
        super().error(traceback.format_exc())

    def setLevel(self, level_str):
        self.level = cvt_logging_level(level_str)
        super().setLevel(self.level)

    def set_logfile(self, filepath):
        self.log_path = filepath
        file_handler = logging.FileHandler(self.log_path)
        file_handler.setFormatter(self.formatter)
        self.addHandler(file_handler)


def cvt_logging_level(level_str):
    level_str = level_str.lower()
    cvt_dict = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
    }

    return cvt_dict[level_str]