"""
    生成随机的uuid，没有中间的'-'
"""
import uuid


def genid():
    return str(uuid.uuid4()).replace('-', '')