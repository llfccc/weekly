from django.conf.urls import url
from .views import InsertWork, GetDevEvent, GetProjects,DelWork,Test,GetEventTypes,GetEventExcel
from .views import GetSaleEvents,GetCustomers,GetSaleActiveTypes
from .views import GetWeeklySummary,InsertSummary,GetSalePhases
from api.views import InsertCustomer,InsertSaleEvent,DelSaleEvent,DelSummary
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    url(r'get_dev_events/', permission_required('api.view_devevent')(GetDevEvent.as_view()), name="api_get_dev_events"),
    url(r'get_projects/', permission_required('api.view_devproject')(GetProjects.as_view()), name="api_get_projects"),
    url(r'get_event_types/', permission_required('api.api.view_deveventtype')(GetEventTypes.as_view()), name="api_get_works"),
    url(r'insert_work/', permission_required('api.add_devevent')(InsertWork.as_view()), name="api_insert_work"),
    url(r'del_work/', permission_required('api.delete_devevent')(DelWork.as_view()), name="api_DelWork"),

    url(r'get_event_excel/', permission_required('api.export_excel')(GetEventExcel.as_view()), name="api_get_works"),
    url(r'get_weekly_summary/',permission_required('api.view_weeksummary')(GetWeeklySummary.as_view()), name="api_get_works"),
    url(r'get_sale_phases/', permission_required('api.view_salephase')(GetSalePhases.as_view()), name="api_get_works"),
    url(r'insert_sale_event/', InsertSaleEvent.as_view(), name="api_get_works"),
    url(r'insert_summary/', InsertSummary.as_view(), name="api_InsertWork"),
    url(r'del_summary/', DelSummary.as_view(), name="api_DelSaleEvent"),  
    url(r'insert_customer/', InsertCustomer.as_view(), name="api_DelWork"),
    url(r'del_sale_event/', DelSaleEvent.as_view(), name="api_DelSaleEvent"),  
    url(r'get_saleevents/', GetSaleEvents.as_view(), name="api_get_works"),
    url(r'insert_customer/', InsertCustomer.as_view(), name="api_insert_customer"),
    url(r'get_customers/', GetCustomers.as_view(), name="api_get_works"),
    url(r'get_sale_event_types/', GetSaleActiveTypes.as_view(), name="api_get_works"),

    #url(r'get_excel/', GetExcel.as_view(), name="api_GetExcel"),
    url(r'^test/', Test.as_view(), name="test"),
]
