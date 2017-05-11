# coding:utf-8
import os
import json
from django.http import HttpResponse, FileResponse, Http404
import datetime
from django.views.generic import View
from utils.tools import my_response, queryset_to_dict, dict_to_json, getMondaySunday
from utils.export_excel import ReportExcel
from .models import DevEvent, DevProject, DevEventType
from .models import   SaleCustomer, SalePhase, SaleTarget, SaleEvent, SaleActiveType
from .models import WeekSummary
from django.db.models import Q
import StringIO
import pandas as pd
from django.core.cache import cache
from django.db import connection, transaction


# import weekly.settings.PROJECT_ROOT as PROJECT_ROOT

# sql 获取数据


def fetch_data(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        col_names = [desc[0] for desc in cursor.description]

        sql_result = cursor.fetchall()
        results = []

        for row in sql_result:
            if row is None:
                break
            results.append(dict(zip(col_names, row)))
    return results


# Create your views here.


class GetWorks(View):
    '''
    查询每日工作内容
    '''

    def get(self, request):

        getParams = request.GET
        project_name = getParams.get('project_name', '')
        filter_date = getParams.get('filterDate', '')
        # 创建查询条件
        where_condition = ''
        if filter_date:
            try:
                start_date = filter_date[:10]
                end_date = filter_date[13:]
            except:
                start_date, end_date = getMondaySunday()
        else:
            start_date, end_date = getMondaySunday()
        where_condition = u'dev.event_date>="{0}" and dev.event_date<="{1}" '.format(start_date, end_date)
        if project_name:
            where_condition += "and project_name like '%{0}%'".format(project_name)


        dev_event_field = ["dev.id as dev_event_id", "description", "event_date", "start_time", "end_time",
                           "fin_percentage", "up_reporter_id", "down_reporter_ids", "dev_event_remark",
                           "dev_event_create_time",
                           "dev_event_owner_id", "dev_event_project_id", "dev_event_type_id"]
        project_field = ["project_name"]
        event_type_field = ["event_type_name"]
        #没有完成显示出对应的上下游对接人
        # up_user_field=["chinese_name as up_reporter_name "]
        # down_user_field = ["chinese_name as down_reporter_name "]
        all_select_field = dev_event_field + project_field + event_type_field

        select_param = ",".join(all_select_field)

        plain_sql = u"SELECT {0} FROM api_devevent as dev left join api_devproject as pro on dev.dev_event_project_id = pro.id \
            left join api_deveventtype on dev.dev_event_type_id = api_deveventtype.id where {1} order by dev.event_date,dev.start_time;".format(
            select_param, where_condition)
        # print(plain_sql)
        row = fetch_data(plain_sql)

        content = dict_to_json(row)

        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class GetProjects(View):
    '''
    查询所有项目属性
    '''

    def get(self, request):
        data = DevProject.objects.all()
        query_field = ["id", "creater_id", "status", "dev_project_remark", "project_name", "create_time"]
        data_dict = queryset_to_dict(data, query_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class GetEventTypes(View):
    '''
    查询所有项目属性
    '''

    def get(self, request):
        data = DevEventType.objects.all()
        query_field = ["id", "creator_id", "event_type_name", "dev_event_type_remark", "create_time"]
        data_dict = queryset_to_dict(data, query_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class InsertWork(View):
    def post(self, request):
        # sid = request.COOKIES.get("sid")
        # username = cache.get(sid).get("username")
        data = request.POST
        print(data)
        insert_field = ["description", "event_date", "start_time", "end_time", "fin_percentage", "up_reporter_id",
                        "down_reporter_ids", "dev_event_remark", "dev_event_project_id", "dev_event_type_id"]
        result = {}
        for t in insert_field:
            result[t] = data.get(t)

        result['dev_event_owner_id'] = 1
        content = {"id": 0}
        if result:
            inset_process = DevEvent(**result)
            try:
                inset_process.save()
                content = {"id": inset_process.id}
                response = my_response(code=0, msg=u"success", content=content)
            except:
                response = my_response(code=1, msg=u"error", content=content)
        return response


class DelWork(View):
    def post(self, request):
        data = request.POST
        print(data)
        delID = data.get("delID")
        del_event_id = DevEvent.objects.filter(id=delID).delete()
        print(del_event_id[0])
        if del_event_id[0] == 0:
            response = my_response(code=1, msg=u"删除失败")
        else:
            content = {"id": del_event_id[0]}
            response = my_response(code=0, msg=u"success", content=content)
        return response


class Test(View):
    def get(self, request):
        return HttpResponse("ok")


class GetSaleEvents(View):
    ''''
    查询拜访记录
    '''

    def get(self, request):
        param = "*"
        plain_sql = "SELECT {0} FROM api_saleevent as sale left join api_saleactivetype as type on sale.active_type_id = type.id \
            left join api_salecustomer as customer on sale.sale_customer_id = customer.id \
            left join api_salephase as phase on sale.sale_phase_id = phase.id ;".format(param)
        row = fetch_data(plain_sql)
        # query_field = ["id", "project_name", "description", "start_time", "end_time", "fin_percentage", "up_reporter_id", "down_reporter_ids",
        #        "event_name", "dev_event_remark"]
        content = dict_to_json(row)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class GetCustomers(View):
    def get(self, request):
        data = SaleCustomer.objects.all()
        query_field = ["id", "full_name", "contact_post", "contact_name", "contact_mdn", "contact_tel_num",
                       "sale_customer_remark", "create_time"]
        data_dict = queryset_to_dict(data, query_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class GetSaleActiveTypes(View):
    def get(self, request):
        data = SaleActiveType.objects.all()
        query_field = ["id", "active_type_name", "sale_active_type_remark", "create_time"]
        data_dict = queryset_to_dict(data, query_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


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


class GetWeeklySummary(View):
    '''
    查询所有项目属性
    '''

    def get(self, request):
        data = WeekSummary.objects.all()
        query_field = ["id", "start_time", "end_time", "summary", "self_evaluation", "plan", "create_time"]
        data_dict = queryset_to_dict(data, query_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response

class InsertSummary(View):
    def post(self, request):
        # sid = request.COOKIES.get("sid")
        # username = cache.get(sid).get("username")
        data = request.POST
        print(data)
        insert_field = ["start_time", "end_time", "summary", "self_evaluation", "plan"]
        result = {}
        for t in insert_field:
            result[t] = data.get(t)

        result['summary_owner_id'] = 1
        content = {"id": 0}
        if result:
            inset_process = WeekSummary(**result)
            try:
                inset_process.save()
                content = {"id": inset_process.id}
                response = my_response(code=0, msg=u"success", content=content)
            except:
                response = my_response(code=1, msg=u"error", content=content)
        return response

class GetEventExcel(View):
    '''
    查询每日工作内容
    '''

    def get(self, request):

        getParams = request.GET
        project_name = getParams.get('project_name', '')
        filter_date = getParams.get('filterDate', '')
        # 创建查询条件
        where_condition = ''
        if filter_date:
            try:
                start_date = filter_date[:10]
                end_date = filter_date[13:]
            except:
                start_date, end_date = getMondaySunday()
        else:
            start_date, end_date = getMondaySunday()
        where_condition = u'dev.event_date>="{0}" and dev.event_date<="{1}" '.format(start_date, end_date)
        if project_name:
            where_condition += "and project_name like '%{0}%'".format(project_name)


        dev_event_field = ["dev.id as dev_event_id", "description", "event_date", "start_time", "end_time",
                           "fin_percentage", "up_reporter_id", "down_reporter_ids", "dev_event_remark",
                           "dev_event_create_time",
                           "dev_event_owner_id", "dev_event_project_id", "dev_event_type_id"]
        project_field = ["project_name"]
        event_type_field = ["event_type_name"]
        #没有完成显示出对应的上下游对接人
        # up_user_field=["chinese_name as up_reporter_name "]
        # down_user_field = ["chinese_name as down_reporter_name "]
        all_select_field = dev_event_field + project_field + event_type_field

        select_param = ",".join(all_select_field)

        plain_sql = u"SELECT {0} FROM api_devevent as dev left join api_devproject as pro on dev.dev_event_project_id = pro.id \
            left join api_deveventtype on dev.dev_event_type_id = api_deveventtype.id where {1} order by dev.event_date,dev.start_time;".format(
            select_param, where_condition)
        # print(plain_sql)
        row = fetch_data(plain_sql)
        # Create a Pandas dataframe from the data.
        df = pd.DataFrame.from_dict(row)
        #create an output stream
        output = StringIO.StringIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        #taken from the original question
        df.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1")
        # workbook = writer.book
        # worksheet = writer.sheets["Sheet_1"]
        # format = workbook.add_format()
        # format.set_bg_color('#eeeeee')
        # worksheet.set_column(0,9,28)
        #the writer has done its job
        writer.close()
        #go back to the beginning of the stream
        output.seek(0)
        response = FileResponse(output.read())
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
            'output.xlsx')
        return response