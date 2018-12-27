"""
    自定义异常的基类
"""
from flask import request, json
from werkzeug.exceptions import HTTPException


class BaseApiException(HTTPException):
    code = 500
    msg = '未知错误'
    status_code = 1
    data = None
    headers = ('Content-Type', 'application/json')

    def __init__(self, code=None, msg=None,status_code=None, data=None, headers=None):
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code
        if msg:
            self.msg = msg
        if not data:
            self.data = request.method + ' ' + self.get_url_no_params()
        else:
            self.data = data
        if headers:
            self.headers = headers
        super(BaseApiException, self).__init__(description=self.msg, response=None)

    def get_body(self, environ=None):
        body = dict(
            # code = self.code, # http请求的状态码
            msg = self.msg,
            status_code = self.status_code, #本次请求的状态码
            data = self.data
        )
        return json.dumps(body)

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [self.headers]

    @staticmethod
    def get_url_no_params():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
