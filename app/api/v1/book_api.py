"""
    book视图函数
"""
from flask import request, jsonify, current_app, json

from app.libs.init_redis import redis_store
from app.libs.redprint import Redprint

# 实例化自定义红图
from app.libs.token_auth import auth
from app.libs.wyy_exception import SuccessException
from app.models.book_model import BookModel
from app.models.user_model import UserModel
from app.validates.forms import BookForm

api = Redprint('book')


@api.route('/add_book', methods=['POST'])
@auth.login_required
def add_book():
    BookForm().validate_for_api()
    BookModel.add_book(request.json)
    return SuccessException()


@api.route('/all_book', methods=['POST'])
def all_book():
    redis_store.set('wyy', json.dumps({'name':'王一扬', 'age': 200}))
    books = BookModel.query.filter_by().all()
    return redis_store.get('wyy')


@api.route('/get_redis_wyy', methods=['GET'])
def get_redis_wyy():
    # redis_store.delete('wyy')
    return redis_store.get('wyy') or '时间'
