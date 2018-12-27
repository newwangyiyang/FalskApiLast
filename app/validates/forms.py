"""
    参数验证模块
"""
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, IntegerField, FloatField, FileField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError

from app.libs.upload_file import set_file
from app.libs.enums import ClientTypeEnum, ScopeEnum
from app.models.user_model import UserModel
from .base_form import BaseForm


class UserSaveForm(BaseForm):
    user_role = IntegerField()
    user_name = StringField(validators=[DataRequired(), Length(min=2, max=6)])
    user_phone = StringField(validators=[DataRequired(), Length(min=11, max=11), Regexp(regex=r'^1\d{10}$')])
    password = StringField(validators=[DataRequired(), Length(min=6, max=30)])

    def validate_user_role(self, field):
        if not field.data:
            return False
        try:
            role = ScopeEnum(field.data)
        except ValueError as e:
            raise e
        self.user_role.data = role


class ClientForm(BaseForm):
    """
        继承自BaseForm
    """
    account = StringField(validators=[DataRequired(message='账号为必传选项'), Length(min=5, max=32)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, field):
        """
            对type进行自定义验证器
            :return:
        """
        try:
            client = ClientTypeEnum(field.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[Email(message='邮箱地址错误')])
    secret = StringField(validators=[DataRequired(), Regexp(r'^[0-9a-zA-Z_*&$#@]{6,22}$')])
    nickname = StringField(validators=[DataRequired(), Length(min=2, max=22)])

    def validate_account(self, field):
        if UserModel.query.filter_by(email=field.data).first():
            raise ValidationError(message='用户名已注册')


class BookForm(BaseForm):
    title = StringField(validators=[Length(min=1, max=50)])
    price = FloatField(validators=[DataRequired()])
    author = StringField(validators=[DataRequired(), Length(min=1, max=30)])


class TokenForm(BaseForm):
    token = StringField(validators=[DataRequired()])


class MyFileForm(BaseForm):
    file = FileField(validators=[FileRequired(message='图片为必传字段'), FileAllowed(set_file, message='只能上传图片')])