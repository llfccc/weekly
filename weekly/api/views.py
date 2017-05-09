# coding:utf-8
import os
import json
from django.http import HttpResponse, FileResponse, Http404

from django.views.generic import View
from utils.tools import my_response, queryset_to_dict, dict_to_json
from utils.export_excel import ReportExcel
from .models import DevEvent,DevProject,DevEventType
from django.db.models import Q
import StringIO
from django.core.cache import cache
from django.db import connection, transaction

# import weekly.settings.PROJECT_ROOT as PROJECT_ROOT

# sql 获取数据


def fetch_data(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        col_names = [desc[0] for desc in cursor.description]

        sql_result = cursor.fetchall()
        results=[]

        for row in sql_result:
            if row is None:
                break   
            results.append(dict(zip(col_names, row)))
    return results
# Create your views here.


class GetWorks(View):
    def get(self, request):
        
        param = "*"
        plain_sql = "SELECT {0} FROM api_devevent as dev left join api_devproject as pro on dev.project_id = pro.id \
            left join api_deveventtype on dev.event_type_id = api_deveventtype.id ;".format(param)
        row = fetch_data(plain_sql)

        query_field = ["id", "project_name", "description", "start_time", "end_time", "fin_percentage", "up_reporter_id", "down_reporter_ids",
               "event_name", "dev_event_remark"]

        data_dict = dict_to_json(row)
        content = data_dict
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class GetProjects(View):
    def get(self, request):   
        data = DevProject.objects.all()
        query_field = ["id","creater_id","status","dev_project_remark","project_name", "create_time"]
        data_dict = queryset_to_dict(data, query_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response

class GetEventTypes(View):
    def get(self, request):   
        data = DevEventType.objects.all()
        query_field = ["id","creator_id","event_type_name","dev_event_type_remark", "create_time"]
        data_dict = queryset_to_dict(data, query_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response

class InsertWork(View):
    def post(self, request):
        # sid = request.COOKIES.get("sid")
        # username = cache.get(sid).get("username")
        data = request.POST
        insert_field=["description","start_time","end_time","fin_percentage","up_reporter_id","down_reporter_ids","dev_event_remark","project_id","event_type_id"]
        result={}
        for t in insert_field:
            result[t]=data.get(t)

        # result['project']=DevProject.objects.get(pk=result['project'])
        # result['event_type']=DevEventType.objects.get(pk=result['event_type'])
        result['owner_id']=1
        content = {"id": 0}
        if result:
            inset_job = DevEvent(**result)
            try:
                inset_job.save()
                content = {"id": inset_job.id}
                response = my_response(code=0, msg=u"success", content=content)                
            except:
                response = my_response(code=1, msg=u"error", content=content)

        return response


class HideWork(View):
    def post(self, request):
        data = request.POST
        print(data)
        hidedid = data.get("hidedid")
        DevEvent.objects.filter(id=hidedid).update(hided=1)
        response = HttpResponse("yes no")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "Access-Control-Allow-Origin, x-requested-with, content-type"
        return response


class Test(View):
    def get(self, request):
        return HttpResponse("ok")


class GetExcel(View):
    def get(self, request):
        sid = request.COOKIES.get("sid")
        username = cache.get(sid).get("username")
        data = request.POST
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        if not start_time:
            start_time = '2017-4-26'
        if not end_time:
            end_time = '2017-4-30'
        data = DevEvent.objects.filter(Q(start_time__gte=start_time) | Q(end_time__lte=end_time)).filter(
            operator=username).all()
        query_field = ["work_title", "complete_status"]
        data_dict = queryset_to_dict(data, query_field)

        output = StringIO.StringIO()
        excel_instance = ReportExcel(output)
        excel_instance.write_excel(data_dict)
        output.seek(0)

        response = FileResponse(output.read())
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
            'output.xlsx')
        return response
