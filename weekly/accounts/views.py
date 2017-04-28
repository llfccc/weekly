# coding=utf-8
from django.shortcuts import render
from django.views import View
from utils.tools import my_response


# Create your views here.
class LoginHandler(View):
    def post(self, request):
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return my_response(code=1, msg=u"密码账号不能为空！")
        print(username + "***" + password)
        content = ''
        if username == 'admin' and password == 'admin':
            response = my_response(code=0, msg="登录成功！", content=content)
            response.set_cookie('username', {'username': "admin", 'sdf': 23434, 'hha': 3434}, 3600)
            return response

        return my_response(code=1, msg="密码错误", content="")

    @staticmethod
    def _encrypt_password(password):
        nb = bytes(password).encode("utf-8")
        sh = hashlib.sha1()
        sh.update(nb)
        crr = sh.digest()
        return base64.b64encode(crr)
