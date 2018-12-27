"""
    自定义异常，继承HTTPException
    自定义返回状态及json格式
"""
from app.libs.base_exception import BaseApiException


class ParameterException(BaseApiException):
    """
        请求参数异常类
    """
    code = 400
    msg = ''
    status_code = 1


class SuccessException(BaseApiException):
    """
        请求成功的数据接口
    """
    code = 200
    msg = '操作成功'
    status_code = 0
    data = None


class ServerException(BaseApiException):
    code = 500
    msg = '服务器错误'
    status_code = 1


class UserNotFoundException(BaseApiException):
    code = 404
    msg = '用户未找到'
    status_code = 1


class AuthFailedException(BaseApiException):
    code = 401
    msg = '密码错误'
    status_code = 1

class ForbiddenException(BaseApiException):
    code = 403
    msg = '禁止访问'
    status_code = 1