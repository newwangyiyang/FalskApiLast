"""
    flask项目的入口app
"""
from flask import current_app
from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.base_exception import BaseApiException
from app.libs.wyy_exception import ServerException

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    """
        此处捕获全局的异常信息
    """
    current_app.logger.exception(e)
    if isinstance(e, BaseApiException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        status_code = 1
        return BaseApiException(code=code, msg=msg, status_code=status_code)
    else:
        # 服务器的全局异常
        if not app.config['DEBUG']:
            # 在生产模式只抛出json格式的异常信息
            return ServerException()
        else:
            # 在开发模式抛出详细的异常信息
            raise e


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088, debug=app.config['DEBUG'])
