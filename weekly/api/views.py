# coding:utf-8
import json

from django.shortcuts import HttpResponse
from django.views.generic import View
from utils.tools import my_response, queryset_to_json
from .models import JobContent


# Create your views here.
class GetWorks(View):

    def get(self, request):
        job_queryset = JobContent.objects.all()
        query_field = ["id", "work_title", "hided"]
        content = queryset_to_json(job_queryset, query_field)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class InsertWork(View):
    def post(self, request):
        data = request.POST
        print(data)
        id = data.get("id")
        work_title = data.get("work_title")
        inset_job = JobContent(id=id, work_title=work_title)
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