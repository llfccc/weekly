from django.conf.urls import url
from .views import InsertWork, GetWorks, GetProjects,DelWork,Test,GetExcel,GetEventTypes
from .views import GetSaleEvents,GetCustomers,GetSaleActiveTypes
from .views import GetWeeklySummary,InsertSummary
urlpatterns = [
    url(r'get_works/', GetWorks.as_view(), name="api_get_works"),
    url(r'get_projects/', GetProjects.as_view(), name="api_get_works"),
    url(r'get_event_types/', GetEventTypes.as_view(), name="api_get_works"),
    url(r'insert_work/', InsertWork.as_view(), name="api_InsertWork"),
    url(r'del_work/', DelWork.as_view(), name="api_DelWork"),

    url(r'get_weekly_summary/', GetWeeklySummary.as_view(), name="api_get_works"),
    # url(r'get_projects/', GetProjects.as_view(), name="api_get_works"),
    # url(r'get_event_types/', GetEventTypes.as_view(), name="api_get_works"),
    url(r'insert_summary/', InsertSummary.as_view(), name="api_InsertWork"),
    # url(r'del_work/', DelWork.as_view(), name="api_DelWork"),

    url(r'get_saleevents/', GetSaleEvents.as_view(), name="api_get_works"),
    url(r'get_customers/', GetCustomers.as_view(), name="api_get_works"),
    url(r'get_sale_event_types/', GetSaleActiveTypes.as_view(), name="api_get_works"),

    url(r'get_excel/', GetExcel.as_view(), name="api_GetExcel"),
    url(r'^test/', Test.as_view(), name="test"),


]
