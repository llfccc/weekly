from django.conf.urls import url
from .views import InsertWork, GetWorks, GetProjects,HideWork,Test,GetExcel,GetEventTypes

urlpatterns = [
    url(r'get_works/', GetWorks.as_view(), name="api_get_works"),
    url(r'get_projects/', GetProjects.as_view(), name="api_get_works"),
    url(r'get_event_types/', GetEventTypes.as_view(), name="api_get_works"),

    url(r'insert_work/', InsertWork.as_view(), name="api_InsertWork"),
    url(r'hide_work/', HideWork.as_view(), name="api_HideWork"),
    url(r'get_excel/', GetExcel.as_view(), name="api_GetExcel"),
    url(r'^test/', Test.as_view(), name="test"),


]
