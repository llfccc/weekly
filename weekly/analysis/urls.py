from django.conf.urls import url
from analysis.views import AnanlysisWorker,AnanlysisProject,AnanlysisLoad,AnanlysisDepartment
from analysis.views import DisplayWeekly,DisplaySaleEvent,GetSalePerformace

urlpatterns = [
    url(r'analysis_worker/', AnanlysisWorker.as_view(), name="api_get_works"),
    url(r'analysis_project/', AnanlysisProject.as_view(), name="api_get_works"),
    url(r'analysis_load/', AnanlysisLoad.as_view(), name="api_get_works"),
    url(r'analysis_department/', AnanlysisDepartment.as_view(), name="api_InsertWork"),
    url(r'display_weekly/', DisplayWeekly.as_view(), name="api_DelWork"),
    url(r'display_sale_event/', DisplaySaleEvent.as_view(), name="analysis_display_sale_event"),

    url(r'get_sale_performance/', GetSalePerformace.as_view(), name="api_get_works"),
    # url(r'get_weekly_summary/', GetWeeklySummary.as_view(), name="api_get_works"),
    # # url(r'get_projects/', GetProjects.as_view(), name="api_get_works"),
    # # url(r'get_event_types/', GetEventTypes.as_view(), name="api_get_works"),
    # url(r'insert_summary/', InsertSummary.as_view(), name="api_InsertWork"),
    # # url(r'del_work/', DelWork.as_view(), name="api_DelWork"),

    # url(r'get_saleevents/', GetSaleEvents.as_view(), name="api_get_works"),
    # url(r'get_customers/', GetCustomers.as_view(), name="api_get_works"),
    # url(r'get_sale_event_types/', GetSaleActiveTypes.as_view(), name="api_get_works"),

    # url(r'get_excel/', GetExcel.as_view(), name="api_GetExcel"),
    # url(r'^test/', Test.as_view(), name="test"),


]
