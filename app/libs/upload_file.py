"""
    配置上传文件的UploadSet
"""
from flask_uploads import UploadSet

set_file = UploadSet('file')
"""新建一个上传用于设置文件类型、过滤等"""