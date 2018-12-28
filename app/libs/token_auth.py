"""
    Token验证
"""
from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.libs.scope import is_in_scope
from app.libs.wyy_exception import AuthFailedException, ForbiddenException

auth = HTTPTokenAuth(scheme='WYY')

User = namedtuple('User', ['user_id', 'scope'])
"""
命名元祖， 该方式的好处是，可通过点语法进行参数的获取
user.user_id
user.scope
"""


def generate_auth_token(user_id, scope='UserScope', expiration=7200):
    """
    生成token
    :param user_id:
    :param scope:默认拥有UserScope权限
    :param expiration:
    :return:
    """
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'user_id': user_id,
        'scope': scope
    })


@auth.verify_token
def verify_token(token):
    """
    在添加了@auth.login_required装饰的视图函数上都会调用该方法，进行权限的验证
    校验token,并将获取到的token进行缓存
    :param token:
    :return:
    """
    user = verigy_auth_token(token)
    if not user:
        return False
    else:
        g.user = user
        return True


def verigy_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailedException(msg='无效token')
    except SignatureExpired:
        raise AuthFailedException(msg='token已失效')
    user_id = data['user_id']
    scope = data['scope']
    allow = is_in_scope(scope, request.endpoint)
    """
    该方法里面是对权限的具体控制，控制每个视图函数，模块对scope的相应开放权限
    """
    if not allow:
        raise ForbiddenException()
    return User(user_id, scope)