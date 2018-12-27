"""
    该文件用来配置权限管理
"""


class BaseScope:
    allow_api = [] # 视图函数级别的权限控制
    forbidden_api = [] # 禁止用户访问哪些视图函数
    allow_module = [] # 模块级别的权限控制

    def __add__(self, others):
        self.allow_api = self.allow_api + others.allow_api
        self.allow_api = list(set(self.allow_api))

        self.allow_module = self.allow_module + others.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden_api = self.forbidden_api + others.forbidden_api
        self.forbidden_api = list(set(self.forbidden_api))
        return self


class UserScope(BaseScope):
    # allow_api = ['v1.user+super_get_user', 'v1.user+get_user', 'v1.user+delete_user']
    forbidden_api = ['v1.user+super_get_user']
    allow_module = ['v1.user', 'v1.book']


class AdminScope(BaseScope):
    # allow_api = [ 'v1.super_get_user' ]
    allow_module = ['v1.user']

    def __init__(self):
        self + UserScope

class SuperAdminScope(BaseScope):
    """
    权限依次递增
    """
    def __init__(self):
        self + AdminScope


def is_in_scope(scope, endpoint):
    # 注意：现在的endpoint的结构是  v1.user+getUser
    scope = globals()[scope]
    # 对传入的scope进行实例化 AdminScope() UserScope() SuperAdminScope()
    red_name = endpoint.split('+')
    module_name = red_name[0]
    if module_name in scope.forbidden_api:
        """
            配置哪些视图函数禁止访问
       """
        return False
    if module_name in scope.allow_module:
        """
            配置一个模块下的所有视图函数都可以被访问
       """
        return True

    if endpoint in scope.allow_api:
        """
            配置视图函数的访问权限
       """
        return True
    else:
        return False