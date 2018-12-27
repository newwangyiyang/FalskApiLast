"""
    imgupload 上传图片模块
"""
import os

from flask import request
from app.libs.upload_file import set_file
from app.libs.redprint import Redprint
from app.utils import gen_uuid

from app.validates.forms import MyFileForm

api = Redprint('imgupload')


@api.route('/img_upload', methods=['POST'])
def img_upload():
    form = MyFileForm()
    form.validate_for_api()
    images = request.files.getlist("file")
    # 多文件上传request.files.getlist('file')
    for image in images:
        suffix = os.path.splitext(image.filename)[1]
        # 生成随机的文件名
        filename = gen_uuid.genid() + suffix
        # 保存文件
        set_file.save(image, name=filename)
        # 获取文件的地址
        img_url = set_file.url(filename)
    return 'success'

"""
# 单文件上传示例
@api.route('/img_upload', methods=['POST'])
def img_upload():
    form = MyFileForm()
    form.validate_for_api()
    image = form.file.data
    suffix = os.path.splitext(image.filename)[1]
    # 生成随机的文件名
    filename = gen_uuid.genid() + suffix
    # 保存文件
    set_file.save(image, name=filename)
    # 获取文件的地址
    img_url = set_file.url(filename)
    return 'success'
"""