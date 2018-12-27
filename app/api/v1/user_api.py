"""
    user的视图函数
"""
from flask import jsonify, g

from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.libs.wyy_exception import SuccessException, AuthFailedException
from app.models.base_model import db
from app.models.user_model import UserModel
from app.validates.forms import UserSaveForm

api = Redprint('user')


@api.route('/save_user', methods=['POST'])
def save_user():
    form = UserSaveForm().validate_for_api()
    UserModel.register_by_phone(user_name=form.user_name.data, user_phone=form.user_phone.data, password=form.password.data, user_role=form.user_role.data)
    return SuccessException()

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
