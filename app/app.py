"""
    创建核心对象app

"""
import uuid
from datetime import date
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from app.libs.wyy_exception import ServerException


class JSONEncoder(_JSONEncoder):
    """
        用于模型对象的序列化
    """
    def default(self, o):
        """
            如果遇到无法序列化的属性，在这里添加对应的方法，例如datetime类型，转化成时间字符串
            :param o:
            :return:
        """
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d %X')
        if isinstance(o, uuid.UUID):
            return str(o)
        else:
            # 不能进行转换则，抛出服务器异常
            raise ServerException()


class Flask(_Flask):
    """
        用于模型对象的序列化
    """
    json_encoder = JSONEncoder


