from django.conf.urls import url
from analysis.viewsDev import AnanlysisEmployeeDevtype,AnanlysisProjectEmployee,AnanlysisProjectTimeTaken,AnanlysisLoad,AnanlysisDepartment,AnanlysisEmployeeEveryday
from analysis.viewsDev import AnalysisDevEvent,AnalysisWeeklySummary
from analysis.viewsDev import AnalysisPosition
from analysis.viewsSale import  DisplaySaleEvent,AnalysisSalePerformace,DisplaySaleTarget
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    url(r'analysis_employee_devtype/', permission_required('api.analysis_devevent')(AnanlysisEmployeeDevtype.as_view()), name="api_get_works"),

    url(r'analysis_employee_everyday/', permission_required('api.analysis_devevent')(AnanlysisEmployeeEveryday.as_view()), name="api_get_works"),

    url(r'analysis_project_employee/', permission_required('api.analysis_devevent')(AnanlysisProjectEmployee.as_view()), name="api_get_works"),
    url(r'analysis_project_timeTaken/', permission_required('api.analysis_devevent')(AnanlysisProjectTimeTaken.as_view()), name="api_get_works"),

    url(r'analysis_load/', permission_required('api.analysis_devevent')(AnanlysisLoad.as_view()), name="api_get_works"),
    url(r'analysis_department/', permission_required('api.analysis_devevent')(AnanlysisDepartment.as_view()), name="api_InsertWork"),
    url(r'analysis_devevent/', permission_required('api.analysis_devevent')(AnalysisDevEvent.as_view()), name="api_DelWork"),
    url(r'analysis_position/', permission_required('api.analysis_devevent')(AnalysisPosition.as_view()), name="api_DelWork"),

    url(r'analysis_sale_performance/', permission_required('api.analysis_sale_event')(AnalysisSalePerformace.as_view()), name="api_get_works"),
    url(r'display_sale_event/', permission_required('api.display_sale_event')(DisplaySaleEvent.as_view()), name="analysis_display_sale_event"),
    url(r'analysis_week_summary/', permission_required('api.analysis_weekly_summary')(AnalysisWeeklySummary.as_view()), name="api_get_works"),

    url(r'display_sale_target/', DisplaySaleTarget.as_view(), name="api_get_works"),

]
