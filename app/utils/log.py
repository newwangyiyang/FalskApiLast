import logging, os
from logging.handlers import RotatingFileHandler


def init_logger(app):
    formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]')
    error_log = os.path.join(os.getcwd() + '/', app.config["ERROR_LOG"])
    if not os.path.exists(os.path.dirname(error_log)):
        os.makedirs(os.path.dirname(error_log))

    error_file_handler = RotatingFileHandler(
        error_log,
        maxBytes=10*1024*1024,
        backupCount=30,
        encoding='utf-8'
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

    info_log = os.path.join(os.getcwd() + '/', app.config["INFO_LOG"])
    if not os.path.exists(os.path.dirname(info_log)):
        os.makedirs(os.path.dirname(info_log))

    info_file_handler = RotatingFileHandler(
        info_log,
        maxBytes=10*1024*1024,
        backupCount=30,
        encoding='utf-8'
    )
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)

    app.logger.setLevel(logging.DEBUG)