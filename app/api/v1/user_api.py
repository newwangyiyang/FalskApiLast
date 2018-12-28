"""
    user的视图函数
"""
from flask import jsonify, g, current_app

from app.libs.redprint import Redprint
from app.libs.token_auth import auth, generate_auth_token
from app.libs.wyy_exception import SuccessException
from app.models.base_model import db
from app.models.user_model import UserModel
from app.validates.forms import UserSaveForm, UserLoginForm

api = Redprint('user')


@api.route('/save_user', methods=['POST'])
def save_user():
    """
    用户注册(user_name, user_phone, password, [user_name])
    """
    form = UserSaveForm().validate_for_api()
    UserModel.register_by_phone(user_name=form.user_name.data, user_phone=form.user_phone.data, password=form.password.data, user_role=form.user_role.data)
    return SuccessException()


@api.route('/login_user', methods=['POST'])
def login_user():
    """
    用户登录(user_phone, password)，获取token
    :return:
    """
    form = UserLoginForm().validate_for_api()
    userObj = UserModel.verify_by_phone(form.user_phone.data, form.password.data) # 获取用户的基本信息{user_id, scope}
    token = generate_auth_token(user_id=userObj['user_id'], scope=userObj['scope'], expiration=current_app.config['TOKEN_EXPIRATION']) # 生成token
    # 注意: 这里的token需要转换格式(默认是字节单位)
    return SuccessException(data=token.decode('ascii'))


@api.route('/get_user_by_token', methods=['POST'])
@auth.login_required
def get_user_by_token():
    """
    根据token来获取用户的基本信息
    :return:
    """
    user = g.user # 从全局里面获取保存的user信息
    user_model = UserModel.query.get(user.user_id) # 获取用户的基本信息，并返回给前端
    return SuccessException(data=user_model)


@api.route('/super_get_user/<uid>', methods=['POST'])
@auth.login_required
def super_get_user(uid):
    user = UserModel.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('/get_user', methods=['POST'])
@auth.login_required
def get_user():
    uid = g.user.uid
    user = UserModel.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('/delete_user', methods=['POST'])
@auth.login_required
def delete_user():
    uid = g.user.uid
    with db.auto_commit():
        user = UserModel.query.filter_by(id=uid).first_or_404()
        user.delete()
    return SuccessException()
