# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django import forms
# fill in custom user info then save it
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from models import UserProfile
# from django.contrib.auth import get_user_model

# 表单


class UserForm(forms.Form):
    username = forms.CharField(label=u'用户名', max_length=100)
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(label=u'用户名', max_length=100)
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput())


# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     mobile = forms.IntegerField(required=True)

#     class Meta:
#         model = UserProfile
#         fields = ('username', 'email', 'password1', 'password2', 'mobile')

#     def save(self, commit=False):
#         user = super(MyRegistrationForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.user_mobile = self.cleaned_data['mobile']
#         user.set_password(self.cleaned_data["password1"])

#         user_default = User.objects.create_user(self.cleaned_data['username'],
#                                                 self.cleaned_data['email'],
#                                                 self.cleaned_data['password1'])
#         user_default.save()

#         if commit:
#              user.save()
#         return user
