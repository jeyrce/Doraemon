# coding=utf-8
"""
__purpose__ = 自定义django中间件
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/20 16:48]
    
    Copyright (c) 2020 JeeysheLu
    
This software is licensed to you under the MIT License. Looking forward to making it better.
"""

__all__ = [
    "ClientInfoMiddleware",
]


class BaseCustomMiddleware(object):
    """
    中间件模板，自定义的中间件继承于此类
    如果需要在处理请求之前做什么事， 需要是实现before_make_response(request)方法
    之后，则实现after_make_response(request)方法
    注意：
        0. 可以实现其中一种方法， 也可两种都不实现
    """

    def __init__(self, get_response):
        # 暂存请求对象
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(self, 'before_make_response'):
            request = self.before_make_response(request)
        response = self.get_response(request)
        if hasattr(self, 'after_make_response'):
            self.after_make_response(request)
        return response


class ClientInfoMiddleware(BaseCustomMiddleware):
    """
    搜集客户端设备信息
    """

    def before_make_response(self, request):
        client_info = {
            "ip": request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR", "0.0.0.0"),
            "device": request.META.get("HTTP_USER_AGENT", "未知设备"),
        }
        setattr(request, "CLIENT", client_info)
        return request
