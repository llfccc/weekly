# coding=utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from utils.tools import my_response, get_random
from forms import UserForm, RegisterForm
from accounts.models import User
from accounts.models import Department
from django.contrib.auth import authenticate
from django.core.cache import cache
from utils.tools import my_response, queryset_to_dict, dict_to_json
from sqljoint.query import departmentname_to_departmentid
from django.contrib import auth
from utils.tools import fetch_data
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
                # login(request, user)
                sid = get_random()
                auth.login(request, user)
                user_object=User.objects.get(username=username)
                try:
                    chinese_name=user_object.chinese_name
                    position_id=user_object.position.id
                    department_id=user_object.department.id
                except:
                    chinese_name=''
                    position_id=''
                    department_id=''
                user_id=user_object.id
                userGroup_sql="select * from accounts_user_groups as ug join auth_group as auth on auth.id=ug.group_id where ug.user_id={0}".format(user_id)

                row = fetch_data(userGroup_sql)
                group_list=[v.get("name") for v in row]
                
                print(group_list)
                content = {"username": username, "chinese_name": chinese_name,\
                           "position_id": position_id, "user_id": user_id,\
                           "department_id":department_id,"group_list":group_list}

                response = my_response(code=0, msg="登录成功！", content=content)
                # login(request, user)
                cache.set(sid, content, timeout=self.cookie_timeout)
                response.set_cookie("sid", sid)  # , max_age=self.cookie_timeout)

                return response
            else:
                return my_response(code=1, msg="账号密码错误！")
        return my_response(code=1, msg="输入内容不合法")


class RegisterHandler(View):
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            # chinese_name = data['chinese_name']
            # group_name = data['group_name']
            password = data['password']
            password2 = data['password']
            print(username)
            if not User.objects.all().filter(username=username):
                    user = User.objects.create_user(username, '', password)
                    user.save() 
                    # login_validate(request, username, password)
                    return my_response(code=0, msg="注册成功", content="")
            else:

                return my_response(code=1, msg="用户已存在", content="")
        return my_response(code=1, msg="用户已存在", content="")


class LogoutHandler(View):
    def get(self, request):
        # username = request.get("username")
        auth.logout(request)
        response = my_response(code=0, msg="用户登出成功",content="")
        response.set_cookie("sid", "", expires=0)
        return response


# 注册
def register(req):
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
    response.delete_cookie('sid')
    return response


class GetUsername(View):
    '''
    查询所有用户中文名或者根据部门名来筛选
    '''
    def get(self, request):   
        getParams = request.GET
        department_id = getParams.get('department_id', '')

        if department_id:
            user_queryset=User.objects.filter(department_id=department_id).all()
        else:
            user_queryset=User.objects.all()
        user_ids=tuple([i.id for i in user_queryset])           
        data = User.objects.filter(pk__in=user_ids).all()

        query_field = ["id","username","chinese_name","department_id", "position_id"]
        data_dict = queryset_to_dict(data, query_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response
