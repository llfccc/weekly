from django.conf.urls import url
from accounts.views import LoginHandler

urlpatterns = [
    url(r'^login/', LoginHandler.as_view()),
]
