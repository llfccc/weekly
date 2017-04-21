from django.shortcuts import render
from django.views import View
from utils.tools import my_response


# Create your views here.
class LoginHandler(View):
    def post(self, request):
        return my_response(code=0, msg="hah")

    @staticmethod
    def _encrypt_password(password):
        nb = bytes(password).encode("utf-8")
        sh = hashlib.sha1()
        sh.update(nb)
        crr = sh.digest()
        return base64.b64encode(crr)
