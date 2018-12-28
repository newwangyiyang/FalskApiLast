"""
    user模型，用于做数据库映射,继承base这个基类
"""
from sqlalchemy import Column, String, SmallInteger, orm
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.enums import ScopeEnum
from app.libs.wyy_exception import UserNotFoundException, AuthFailedException
from app.models.base_model import BaseModel, db
from app.utils.gen_uuid import genid


class UserModel(BaseModel):
    user_id = Column(String(32), primary_key=True)
    user_role = Column(SmallInteger, default=0) # 拥有的权限范围，默认为UserScope
    user_name = Column(String(10), nullable=False)
    user_phone = Column(String(11), nullable=False, unique=True)
    _password = Column('password', String(100))

    @orm.reconstructor
    def __init__(self):
        """
        定义序列化字段
        """
        self.fields = ['user_id', 'user_role', 'user_name', 'user_phone']

    @property
    def password(self):
        """
        对外不公开password属性，
        UserModel.password实际是访问UserModel._password
        :return:
        """
        return self._password

    @password.setter
    def password(self, raw):
        """
        setter方方法加密password
        :param raw:
        :return:
        """
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        """
        校验密码
        :param raw:
        :return:
        """
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    @staticmethod
    def register_by_phone(user_name, user_phone, password, user_role):
        """
            注册新增用户
            :return:
        """
        with db.auto_commit():
            user = UserModel()
            user.set_attrs({'user_id': genid(), 'user_role': user_role, 'user_name': user_name, 'user_phone': user_phone, 'password': password})
            db.session.add(user)

    @staticmethod
    def verify_by_phone(user_phone, password):
        """
        手机号、密码登录，校验权限
        :param user_phone:
        :param password:
        :return:
        """
        user = UserModel.query.filter(user_phone==user_phone).first_or_404()
        if not user.check_password(password): # 校验密码是否正确，校验失败会抛异常
            raise AuthFailedException()
        role = user.user_role
        scope = '' # 校验权限,对接口进行权限控制
        if ScopeEnum(role) == ScopeEnum.UserScope:
            scope = ScopeEnum.UserScope.name
        elif ScopeEnum(role) == ScopeEnum.AdminScope:
            scope = ScopeEnum.AdminScope.name
        elif ScopeEnum(role) == ScopeEnum.SuperAdminScope:
            scope = ScopeEnum.SuperAdminScope.name
        # scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'user_id': user.user_id, 'scope': scope}
