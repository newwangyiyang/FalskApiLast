"""
    配置上传文件的UploadSet
"""
from flask_uploads import UploadSet

set_file = UploadSet('file')
"""
实例化一个上传对象UploadSet,
其中file为每一个UploadSet实例对象的标识
每一个上传图片接口都需要实例话一个新的UploadSet对象
并需要注册到app上
可在配置文件中对那些文件进行允许上传
"""