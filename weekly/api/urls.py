from django.conf.urls import url
from .views import InsertDevWork, GetDevEvent, GetProjects,DelDevEvent,Test,GetEventTypes,GetEventExcel
from .views import GetSaleEvents,GetCustomers,GetSaleActiveTypes
from .views import GetWeeklySummary,InsertSummary,GetSalePhases
from api.views import InsertCustomer,InsertSaleEvent,DelSaleEvent,DelSummary
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    url(r'get_dev_events/', permission_required('api.view_devevent')(GetDevEvent.as_view()), name="api_get_dev_events"),
    url(r'get_projects/', permission_required('api.view_devproject')(GetProjects.as_view()), name="api_get_projects"),
    url(r'get_event_types/', permission_required('api.view_deveventtype')(GetEventTypes.as_view()), name="api_get_works"),
    url(r'insert_devevent/', permission_required('api.insert_devevent')(InsertDevWork.as_view()), name="api_insert_work"),
    url(r'del_devevent/', permission_required('api.delete_devevent')(DelDevEvent.as_view()), name="api_DelWork"),

    url(r'get_event_excel/', permission_required('api.export_excel')(GetEventExcel.as_view()), name="api_get_works"),
    url(r'get_weekly_summary/',permission_required('api.view_weeksummary')(GetWeeklySummary.as_view()), name="api_get_works"),
    url(r'get_sale_phases/', permission_required('api.view_SalePhase')(GetSalePhases.as_view()), name="api_get_works"),
    url(r'insert_sale_event/', permission_required('api.insert_saleevent')(InsertSaleEvent.as_view()), name="api_get_works"),
    url(r'insert_summary/', permission_required('api.insert_weeksummary')(InsertSummary.as_view()), name="api_InsertWork"),
    url(r'del_summary/', permission_required('api.markDel_weeksummary')(DelSummary.as_view()), name="api_DelSaleEvent"),  
    url(r'insert_customer/', permission_required('api.add_salecustomer')(InsertCustomer.as_view()), name="api_DelWork"),
    url(r'del_sale_event/', permission_required('api.delete_saleevent')(DelSaleEvent.as_view()), name="api_DelSaleEvent"),  
    url(r'get_saleevents/', permission_required('api.view_SaleEvent')(GetSaleEvents.as_view()), name="api_get_works"),
    url(r'get_customers/', permission_required('api.view_SaleCustomer')(GetCustomers.as_view()), name="api_get_works"),
    url(r'get_sale_event_types/', permission_required('api.view_SaleActivateType')(GetSaleActiveTypes.as_view()), name="api_get_works"),

    #url(r'get_excel/', GetExcel.as_view(), name="api_GetExcel"),
    url(r'^test/', Test.as_view(), name="test"),
]
