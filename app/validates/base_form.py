"""
    参数校验的基类
"""
from flask import request
from wtforms import Form

from app.libs.wyy_exception import ParameterException


class BaseForm(Form):
    def __init__(self):
        super(BaseForm, self).__init__(request.files, data=request.get_json(silent=True), **request.args.to_dict())

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)
        return self