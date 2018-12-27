"""
    客户端注册
"""
from flask import request, jsonify

from app.libs.enums import ClientTypeEnum
from app.libs.redprint import Redprint
from app.libs.wyy_exception import SuccessException
from app.models.user_model import UserModel
from app.validates.forms import ClientForm, UserEmailForm

api = Redprint('client')


def __create_client_by_email():
    form = UserEmailForm().validate_for_api()
    UserModel.register_by_email(form.nickname.data, form.account.data, form.secret.data)


@api.route('/create_client', methods=['POST'])
def create_client():
    form = ClientForm().validate_for_api() # 在这里对参数校验，如果校验不同过，会自动抛出异常，给前端已明确的提示
    promise = {
        ClientTypeEnum.USER_EMAIL: __create_client_by_email
    }
    promise[form.type.data]()
    return SuccessException()


