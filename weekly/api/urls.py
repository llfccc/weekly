from django.conf.urls import url
from .views import InsertWork, GetWorks, HideWork,Test

urlpatterns = [
    url(r'get_works/', GetWorks.as_view(), name="api_get_works"),
    url(r'insert_work/', InsertWork.as_view(), name="api_InsertWork"),
    url(r'hide_work/', HideWork.as_view(), name="api_HideWork"),
    url(r'^test/', Test),

]
