"""
    核心对象的初始化
"""
import logging

from flask import request
from flask_uploads import configure_uploads, UploadSet

from app.libs.init_redis import init_redis
from app.libs.upload_file import set_file
from app.utils.log import init_logger
from app.utils.param_util import get_request_params, get_url_no_params
from .app import Flask
from flask_cors import CORS

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def init_limiter(app):
    """限制访问视图函数的次数， 每天200次"""
    limiter = Limiter(key_func=get_remote_address, default_limits=['300/day, 20/minute, 10/second'])
    limiter.logger.addHandler(logging.StreamHandler())
    limiter.init_app(app)


def register_blueprint_v1(app):
    """
    注册蓝图
    :param app:
    :return:
    """
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def init_upload(app):
    """将创建的文件上传对象注册到核心对象app上"""
    configure_uploads(app, [ set_file ])
    # configure_uploads(app, [ set_file01, set_file02 ])  注册多个UploadSet实例


def register_plugin(app):
    """
    扩展插件的补充
    :param app:
    :return:
    """
    from app.models.base_model import db
    """数据库连接"""
    ''
    db.init_app(app)
    with app.app_context():
        db.create_all()

    init_limiter(app)
    """限制IP的访问次数，可作用于反爬虫"""

    init_logger()
    """日志初始化"""

    init_upload(app)
    """上传文件初始化"""


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')

    CORS(app)
    """解决跨域问题"""

    init_redis(app)
    """配置redis缓存"""

    @app.before_request
    def before_request():
        """向日志输出每一次请求 请求方式  请求路径  请求参数"""
        app.logger.info('[%s] %s %s' % (request.method, get_url_no_params(request), get_request_params(request)))

    register_blueprint_v1(app)
    register_plugin(app)
    return app