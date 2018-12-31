"""
    create by wangyiyiang
"""


def get_request_params(request):
    """
        已字典的形式获取参数，有即返回，无则返回无参
        :param request:
        :return:
    """
    return request.get_json(silent=True) or request.args.to_dict() or request.form.to_dict() or 'NoParams'


def get_url_no_params(request):
    """获取请求路径"""
    full_path = str(request.full_path)
    main_path = full_path.split('?')
    return main_path[0]