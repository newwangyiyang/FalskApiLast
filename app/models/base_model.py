import datetime
import time
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, String, Integer, BigInteger

from app.libs.wyy_exception import UserNotFoundException
from app.utils.date_util import get_current_timestamp


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if rv is None:
            raise UserNotFoundException()
        return rv

    def first_or_404(self):
        rv = self.first()
        if rv is None:
            raise UserNotFoundException()
        return rv


db = SQLAlchemy(query_class=Query)


class BaseModel(db.Model):
    __abstract__ = True
    create_time = Column(BigInteger, default=get_current_timestamp()) # 保存时间戳(为毫秒级)
    status = Column(SmallInteger, default=0) # 0表正常状态， 可用于逻辑删除


    def __getitem__(self, item):
        """
            用于序列化
        :param item:
        :return:
        """
        return getattr(self, item)

    def keys(self):
        """
            用于序列化
        :return:
        """
        return self.fields

    def hide(self, *args):
        """
            返回前端需要隐藏哪些字段
            例如:
                隐藏id, email字段
            users = [v.hide('id', 'email') for v in users]
            jsonify(books)
            :param hide_value:
            :return:
        """
        for arg in args:
            if arg in self.fields:
                self.fields.remove(arg)
        return self

    def append(self, *args):
        """
            增加返给前端的字段
            :param args:
            :return:
        """
        for arg in args:
            self.fields.append(arg)
        return self

    def set_attrs(self, attrs_dict):
        """
        将字典对象，转成模型Model,不用再去进行一个个的赋值操作
        :param attrs_dict:
        :return:
        """
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        """
        逻辑删除，可执行删除
        :return:
        """
        self.status = 0

