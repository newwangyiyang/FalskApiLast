import logging
import os, time
from logging.handlers import TimedRotatingFileHandler


def init_logger(app):
    LEVELS = {'debug': logging.DEBUG,
              'info':  logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}

    log_dir = os.path.join(app.config['LOG_PATH'])
    log_file = os.path.join(app.config['LOG_PATH'], app.config['LOG_FILENAME'])
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)

    log_level = LEVELS.get(app.config['LOG_LEVEL'].lower(), 'info')

    rotate_handler = TimedRotatingFileHandler(log_file, when='S', interval=1, encoding='utf-8')
    rotate_handler.suffix = "%Y%m%d"
    rotate_handler.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)-10s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s')
    rotate_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    app.logger.addHandler(stream_handler)
    app.logger.addHandler(rotate_handler)

    app.logger.info('初始化日志成功')