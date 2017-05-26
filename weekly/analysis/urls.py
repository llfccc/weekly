from django.conf.urls import url
from analysis.viewsDev import AnanlysisEmployee,AnanlysisProject,AnanlysisLoad,AnanlysisDepartment
from analysis.viewsDev import AnalysisDevEvent,AnalysisWeeklySummary
from analysis.viewsDev import AnalysisPosition
from analysis.viewsSale import  DisplaySaleEvent,AnalysisSalePerformace
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    url(r'analysis_employee/', permission_required('api.analysis_devevent')(AnanlysisEmployee.as_view()), name="api_get_works"),
    url(r'analysis_project/', permission_required('api.analysis_devevent')(AnanlysisProject.as_view()), name="api_get_works"),
    url(r'analysis_load/', permission_required('api.analysis_devevent')(AnanlysisLoad.as_view()), name="api_get_works"),
    url(r'analysis_department/', permission_required('api.analysis_devevent')(AnanlysisDepartment.as_view()), name="api_InsertWork"),
    url(r'analysis_devevent/', permission_required('api.analysis_devevent')(AnalysisDevEvent.as_view()), name="api_DelWork"),
    url(r'analysis_position/', permission_required('api.analysis_devevent')(AnalysisPosition.as_view()), name="api_DelWork"),

    url(r'analysis_sale_performance/', permission_required('api.analysis_sale_event')(AnalysisSalePerformace.as_view()), name="api_get_works"),
    url(r'display_sale_event/', permission_required('api.display_sale_event')(DisplaySaleEvent.as_view()), name="analysis_display_sale_event"),

    url(r'analysis_week_summary/', permission_required('api.analysis_weekly_summary')(AnalysisWeeklySummary.as_view()), name="api_get_works"),
]
