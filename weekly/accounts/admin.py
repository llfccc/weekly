# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
# from models import UserProfile

# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'userprofile'

# class UserProfileAdmin(UserAdmin):
#     inlines = (UserProfileInline, )

# admin.site.register(UserProfile, UserProfileAdmin)

#coding:utf-8
from django.contrib import admin

# Register your models here.
from accounts.models import User
admin.site.register(User)