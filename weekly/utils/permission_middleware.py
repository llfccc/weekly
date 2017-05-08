# !/usr/bin/env python
# !-*-coding:utf-8-*-


import time
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from utils.tools import my_response, Logger


# class PermissionCheck(MiddlewareMixin):
#     """
#         中间件，用于检查请求权限
#     """
#     cookie_time = 2 * 3600

#     @staticmethod
#     def process_request(request):
#         """
#         :param request:
#         :return:
#         """
#         # print "start", time.time()
#         if "login" in request.path:
#             return
#         # request.COOKIES["sid"] = "9342c00a6cb65a2d35e2bd48cc2ab163"
#         sid = request.COOKIES.get("sid")
#         content = cache.get(sid)
#         if content:
#             username = content.get("username")
#             Logger.debug("{0}: request, url is: {1}".format(username, request.path.encode("utf-8")))
#             request.COOKIES["username"] = username
#         else:
#             return my_response(code=-1, msg="登录超时！")

#     @staticmethod
#     def process_response(request, response):
#         sid = request.COOKIES.get("sid")
#         if sid and "logout" not in request.path:
#             cache.expire(sid, timeout=PermissionCheck.cookie_time)
#             response.set_cookie("sid", sid, max_age=PermissionCheck.cookie_time - 10)
#         # print "end time", time.time()
#         return response

class PrintCheck(MiddlewareMixin):
    """
        中间件，用于检查请求权限
    """
    cookie_time = 2 * 3600

    @staticmethod
    def process_request(request):
        print("middleware")
        
