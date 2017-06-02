# coding=utf-8
"""weekly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
# from rest_framework_swagger.views import get_swagger_view
# schema_view = get_swagger_view(title='Pastebin API')

# from xadmin.plugins import xversion
# import xadmin

#version模块自动注册需要版本控制的 Model
# xversion.register_models()

# xadmin.autodiscover()

from django.conf.urls import include,url
from django.contrib import admin
from weekly.views import home



urlpatterns = [
    url(r'^$', home),
    url(r'admin/',admin.site.urls),
    url(r'works/', include('api.urls')),
    url(r'analysis/', include('analysis.urls')),
    url(r'accounts/', include('accounts.urls')),
    # url(r'^$', schema_view)
]


