from django.conf.urls import url
from accounts.views import LoginHandler, RegisterHandler, LogoutHandler,GetUsername
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    url(r'^login/', LoginHandler.as_view()),
    # url(r'^register/', RegisterHandler.as_view()),
    url(r'^logout/', LogoutHandler.as_view()),
    url(r'^get_username/', permission_required('accounts.get_chinesename')(GetUsername.as_view())),
]
