# coding=utf-8
from django import forms
from models import User


# 表单
class UserForm(forms.Form):
    username = forms.CharField(label=u'用户名', max_length=100)
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(label=u'用户名', max_length=100)
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput())
