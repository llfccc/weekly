from django.conf.urls import url
from accounts.views import LoginHandler, RegisterHandler, LogoutHandler

urlpatterns = [
    url(r'^login/', LoginHandler.as_view()),
    url(r'^register/', RegisterHandler.as_view()),
    url(r'^logout/', LogoutHandler.as_view()),
]
