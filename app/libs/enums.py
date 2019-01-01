"""
    定义常用的枚举
"""
from enum import Enum, unique


@unique
class ClientTypeEnum(Enum):
    """
    登录方式枚举类
    """
    USER_EMAIL = 100
    USER_PHONE = 101

    # 微信小程序
    USER_MINI = 200
    # 微信公众号
    USER_WX = 201


@unique
class ScopeEnum(Enum):
    """
    scoped枚举类，用户权限管理
    该权限从数据库里读出
    """
    UserScope = 10
    AdminScope = 100
    SuperAdminScope = 1000
