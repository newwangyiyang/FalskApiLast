"""
    imgupload 上传图片模块
"""
import os

from flask import request, current_app
from app.libs.upload_file import set_file
from app.libs.redprint import Redprint
from app.libs.wyy_exception import SuccessException
from app.utils import gen_uuid

from app.validates.forms import MyFileForm

api = Redprint('imgupload')


# @api.route('/img_upload', methods=['POST'])
# def img_upload():
#     form = MyFileForm().validate_for_api()
#     images = request.files.getlist("file")
#     # 多文件上传request.files.getlist('file')
#     for image in images:
#         suffix = os.path.splitext(image.filename)[1]
#         # 生成随机的文件名
#         filename = gen_uuid.genid() + suffix
#         # 保存文件
#         set_file.save(image, name=filename)
#         # 获取文件的地址
#         img_url = set_file.url(filename)
#     return 'success'

# 单文件上传示例
@api.route('/img_upload', methods=['POST'])
def img_upload():
    form = MyFileForm().validate_for_api()
    image = form.file.data
    suffix = os.path.splitext(image.filename)[1]
    # 生成随机的文件名
    filename = gen_uuid.genid() + suffix
    # 保存文件
    set_file.save(image, name=filename)

    # 获取文件的地址
    img_url = set_file.url(filename)
    return SuccessException(data=img_url, msg='图片上传成功')

"""
# 将文件保存到本地
filename = photos.save(request.files['photo'])
# 返回文件路径
file_url = photos.url(filename)
basename = photos.get_basename(filename)
path = photos.path(filename)
print('file_url =', file_url)  # http://127.0.0.1:8000/_uploads/photos/1525269617847e958494e4a.jpg (线上代理路径)
print('basename =', basename)  # 1525269617847e958494e4a.jpg (名称)  (可在数据库保存该名称)
print('path =', path)  # D:\\Python\\FalskApiLast\\static/upload\\36b9603830e149b8bdce3cf2d1be0ad0.jpg (绝对路径)
"""
