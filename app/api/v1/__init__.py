"""
    蓝图的初始化
"""

from flask import Blueprint

from app.api.v1 import book_api, user_api, client_api, token_api, gift_api, imgupload_api


def create_blueprint_v1():
    v1 = Blueprint('v1', __name__)
    # 自定义视图函数(其中url_prefix可传可不传， 不传会在redprint中进行判断)
    user_api.api.register(v1)
    imgupload_api.api.register(v1)
    # book_api.api.register(v1)
    # client_api.api.register(v1)
    # token_api.api.register(v1)
    # gift_api.api.register(v1)
    return v1
