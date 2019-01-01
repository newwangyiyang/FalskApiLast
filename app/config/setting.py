"""
    用于配置普通项的配置文件
"""
import os

from flask_uploads import IMAGES

TOKEN_EXPIRATION = 30 * 24 * 3600

DEBUG = True

# sqlalchemy
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 设置文件上传
UPLOADED_FILE_DEST = os.path.join(os.getcwd(),'static/upload')
UPLOADED_FILE_ALLOW = IMAGES

#设置log日志
ERROR_LOG = "../logs/error.log"
INFO_LOG = "../logs/info.log"