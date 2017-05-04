# coding=utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from utils.tools import my_response, get_random
from forms import UserForm
from models import User
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache


# Create your views here.
class LoginHandler(View):
    cookie_timeout = 2 * 3600
    def post(self, request):
        uf = UserForm(request.POST)
        if uf.is_valid():
            # 获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                sid = get_random()
                content={"username":username}
                response = my_response(code=0, msg="登录成功！", content=content)
                #login(request, user)
                cache.set(sid, content, timeout=self.cookie_timeout)
                response.set_cookie("sid", sid) #, max_age=self.cookie_timeout)
                return response
            else:
                # 比较失败，还在login
                return my_response(code=1, msg="账号密码错误！")

        data = request.POST
        print(data)
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




class RegisterHandler(View):
    def post(self, request):
        error = []
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                username = data['username']
                chinese_name = data['chinese_name']
                group_name = data['group_name']
                password = data['password']
                password2 = data['password2']
                if not User.objects.all().filter(username=username):
                    if form.pwd_validate(password, password2):
                        user = User.objects.create_user(username, '', password)
                        profile = Profile(chinese_name=chinese_name, group_name=group_name, user_id=user.id)
                        profile.save()

                        user.save()
                        # login_validate(request, username, password)
                        return render_to_response('welcome.html', {'user': username})
                    else:
                        error.append('Please input the same password')
                else:
                    error.append(
                        'The username has existed,please change your username')
        else:
            form = RegisterForm()
        return render_to_response('register.html', {'form': form, 'error': error})

        return my_response(code=1, msg="密码错误", content="")


class LogoutHandler(View):
    def get(self, request):
        # username = request.get("username")
        response = my_response(code=0, msg="用户登出成功.")
        response.set_cookie("sid", "", expires=0)
        return response


# 注册
def regist(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            # 获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 添加到数据库
            User.objects.create(username=username, password=password)
            return HttpResponse('regist success!!')
    else:
        uf = UserForm()
    return render_to_response('regist.html', {'uf': uf}, context_instance=RequestContext(req))


# 登陆成功
def index(req):
    username = req.COOKIES.get('username', '')
    return render_to_response('index.html', {'username': username})


# 退出
def logout(req):
    response = HttpResponse('logout !!')
    # 清理cookie里保存username
    response.delete_cookie('username')
    return response
