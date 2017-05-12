from django.conf.urls import url
from .views import InsertWork, GetWorks, GetProjects,DelWork,Test,GetEventTypes,GetEventExcel
from .views import GetSaleEvents,GetCustomers,GetSaleActiveTypes
from .views import GetWeeklySummary,InsertSummary,GetSalePhases
from api.views import InsertCustomer,InsertSaleEvent,DelSaleEvent
urlpatterns = [
    url(r'get_works/', GetWorks.as_view(), name="api_get_works"),
    url(r'get_projects/', GetProjects.as_view(), name="api_get_works"),
    url(r'get_event_types/', GetEventTypes.as_view(), name="api_get_works"),
    url(r'insert_work/', InsertWork.as_view(), name="api_InsertWork"),
    url(r'del_work/', DelWork.as_view(), name="api_DelWork"),

    url(r'get_event_excel/', GetEventExcel.as_view(), name="api_get_works"),
    url(r'get_weekly_summary/', GetWeeklySummary.as_view(), name="api_get_works"),
    url(r'get_sale_phases/', GetSalePhases.as_view(), name="api_get_works"),
    url(r'insert_sale_event/', InsertSaleEvent.as_view(), name="api_get_works"),
    url(r'insert_summary/', InsertSummary.as_view(), name="api_InsertWork"),

    url(r'insert_customer/', InsertCustomer.as_view(), name="api_DelWork"),
    url(r'del_sale_event/', DelSaleEvent.as_view(), name="api_DelSaleEvent"),  
    url(r'get_saleevents/', GetSaleEvents.as_view(), name="api_get_works"),
    url(r'insert_customer/', InsertCustomer.as_view(), name="api_insert_customer"),
    url(r'get_customers/', GetCustomers.as_view(), name="api_get_works"),
    url(r'get_sale_event_types/', GetSaleActiveTypes.as_view(), name="api_get_works"),

    #url(r'get_excel/', GetExcel.as_view(), name="api_GetExcel"),
    url(r'^test/', Test.as_view(), name="test"),
]
