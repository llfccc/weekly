# coding:utf-8
import os
from django.http import  HttpResponse ,FileResponse,Http404

from django.views.generic import View
from utils.tools import my_response, queryset_to_dict, dict_to_json, ReportExcel
from .models import JobContent
from django.db.models import Q
# import weekly.settings.PROJECT_ROOT as PROJECT_ROOT


# Create your views here.
class GetWorks(View):
    def get(self, request):
        job_queryset = JobContent.objects.all()
        query_field = ["id", "work_title", "start_time", "end_time", "hided", "complete_status"]
        data_list = queryset_to_dict(job_queryset, query_field)
        content = dict_to_json(data_list)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class InsertWork(View):
    def post(self, request):
        data = request.POST
        print(data)
        work_title = data.get("work_title")
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        complete_status = data.get("complete_status")
        content = "bad"
        if work_title:
            inset_job = JobContent(work_title=work_title, start_time=start_time, end_time=end_time,
                                   complete_status=complete_status)
            inset_job.save()
            content = {"id": inset_job.id}
        # return HttpResponse(json.dumps(content))
        response = my_response(code=0, msg=u"success", content=content)
        return response


class HideWork(View):
    def post(self, request):
        data = request.POST
        print(data)
        hidedid = data.get("hidedid")
        JobContent.objects.filter(id=hidedid).update(hided=1)
        response = HttpResponse("yes no")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "Access-Control-Allow-Origin, x-requested-with, content-type"
        return response


def Test(response):
    return HttpResponse("ok")


class GetExcel(View):
    def get(self, request):
        data = request.POST
        print(data)
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        if not start_time:
            start_time = '2017-4-26'
        if not end_time:
            end_time = '2017-4-30'
        data = JobContent.objects.filter(Q(start_time__gte=start_time) | Q(end_time__lte=end_time)).all()
        query_field = ["work_title", "complete_status"]
        data_dict = queryset_to_dict(data, query_field)

        excel_instance = ReportExcel()
        excel_instance.write_excel(data_dict)

        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        output_filename = PROJECT_ROOT + r'\hello.xlsx'
        response = FileResponse(open(output_filename, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format('hello.xlsx')
        return response
