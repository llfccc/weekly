from django.conf.urls import url
from accounts.views import LoginHandler, RegisterHandler, LogoutHandler,GetUsername
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^login/', LoginHandler.as_view()),
    # url(r'^register/', RegisterHandler.as_view()),
    url(r'^logout/', LogoutHandler.as_view()),
    url(r'^get_username/', permission_required('accounts.view_chinesename')(cache_page(60 * 60)(GetUsername.as_view()))),
]
