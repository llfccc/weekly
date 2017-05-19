# coding:utf-8
import os
import json
import re
from django.http import HttpResponse, FileResponse, Http404
import datetime
from django.views.generic import View
from utils.tools import my_response, queryset_to_dict, dict_to_json
from utils.export_excel import ReportExcel
from utils.tools import fetch_data,get_user_id,getfirstday
from .models import DevEvent, DevProject, DevEventType
from .models import   SaleCustomer, SalePhase, SaleTarget, SaleEvent, SaleActiveType
from .models import WeekSummary
from django.db.models import Q
import StringIO
import pandas as pd
from django.core.cache import cache
from django.db import connection, transaction
from accounts.models import User
from sqljoint.query import join_sql

# Create your views here.


class GetWorks(View):
    '''
    查询每日工作内容
    '''

    def get(self, request):
        user_id=get_user_id(request)
        getParams = request.GET
        project_name = getParams.get('project_name', '')
        filter_date = getParams.get('filter_date', '')
        #没有完成显示出对应的上下游对接人
        # up_user_field=["chinese_name as up_reporter_name "]
        # down_user_field = ["chinese_name as down_reporter_name "]
        plain_sql=join_sql(filter_date,project_name,'','',user_id)

        query_result = fetch_data(plain_sql)
        #将down_reporter_ids由id对应具体的人
        for row in query_result:
            down_reporter_id_list= row['down_reporter_ids'].split(',')
            down_reporter_name_list=[]
            
            for i in down_reporter_id_list:
                down_reporter_name=User.objects.get(id=i).chinese_name
                if down_reporter_name:
                        down_reporter_name_list.append(down_reporter_name)                
            row['down_reporter_ids']=','.join(down_reporter_name_list)
        
        content = dict_to_json(query_result)

        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class GetProjects(View):
    '''
    查询所有项目属性
    '''

    def get(self, request):
        data = DevProject.objects.filter(project_is_closed=False).all()
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
        data = DevEventType.objects.filter(devEventType_is_closed=False).all()
        query_field = ["id", "creator_id", "event_type_name", "dev_event_type_remark", "create_time"]
        data_dict = queryset_to_dict(data, query_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class InsertWork(View):
    def post(self, request):
        user_id=get_user_id(request)        
        data = request.POST
        print(data)
        insert_field = ["description", "event_date", "start_time", "end_time", "fin_percentage", "up_reporter_id",
                        "down_reporter_ids", "dev_event_remark", "dev_event_project_id", "dev_event_type_id"]
        result = {}
        for t in insert_field:
            result[t] = data.get(t)

        result['dev_event_owner_id'] = user_id
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
        user_id=get_user_id(request)
        data = request.POST
        print(data)
        delID = data.get("delID")
        del_event = DevEvent.objects.get(id=delID)
        print(del_event.id)
        if del_event.dev_event_owner_id==user_id:
            del_event_id=del_event.delete()
        else:
            response = my_response(code=1, msg=u"你不是该记录的所有人")

        if del_event_id[0] == 0:
            response = my_response(code=1, msg=u"删除失败，可能已经不存在")
        else:
            content = {"id": del_event_id[0]}
            response = my_response(code=0, msg=u"删除成功", content=content)
        return response


class Test(View):
    def get(self, request):
        return HttpResponse("ok")


class GetSaleEvents(View):
    ''''
    查询拜访记录
    '''

    def get(self, request):
        user_id=get_user_id(request)
        param = "*,sale.id as sale_event_id"
        plain_sql = "SELECT {0} FROM api_saleevent as sale left join api_saleactivetype as type on sale.active_type_id = type.id \
            left join api_salecustomer as customer on sale.sale_customer_id = customer.id \
            left join api_salephase as phase on sale.sale_phase_id = phase.id \
            where sale_event_owner_id={1};".format(param,user_id)
        row = fetch_data(plain_sql)
        # query_field = ["id", "project_name", "description", "start_time", "end_time", "fin_percentage", "up_reporter_id", "down_reporter_ids",
        #        "event_name", "dev_event_remark"]
        content = dict_to_json(row)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response

class InsertCustomer(View):
    def post(self, request):
        user_id=get_user_id(request)
        content = {"id": 0}
        data = request.POST
        print(data)
        insert_field = ["full_name", "short_name","contact_post", "contact_name", "contact_mdn", "contact_tel_num",
                       "sale_customer_remark"]
        result = {}
        for t in insert_field:
            result[t] = data.get(t)
        customer_exist=SaleCustomer.objects.filter(full_name=result['full_name']).all()
        print(customer_exist)
        if customer_exist:
            response = my_response(code=1, msg=u"公司全称已存在")
            return response
        result['sale_customer_owner_id'] = user_id
        
        if result:
            inset_process = SaleCustomer(**result)
            try:
                inset_process.save()
                content = {"id": inset_process.id}
                response = my_response(code=0, msg=u'恭喜你，新增成功', content=content)
            except:
                response = my_response(code=1, msg=u'插入失败', content=content)
        return response

class GetCustomers(View):
    def get(self, request):
        user_id=get_user_id(request)

        query_field = ["id", "full_name", "short_name","contact_post", "contact_name", "contact_mdn", "contact_tel_num",
                       "sale_customer_remark", "create_time"]
        data = SaleCustomer.objects.filter(sale_customer_owner_id=user_id).all()
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


class GetSalePhases(View):
    def get(self, request):
        data = SalePhase.objects.all()
        query_field = ["id", "phase_name", "description","phase_count","sale_phase_remark" , "create_time"]
        data_dict = queryset_to_dict(data, query_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


# class GetExcel(View):
#     def get(self, request):
#         sid = request.COOKIES.get("sid")
#         username = cache.get(sid).get("username")
#         data = request.POST
#         start_time = data.get("start_time")
#         end_time = data.get("end_time")
#         if not start_time:
#             start_time = '2017-4-26'
#         if not end_time:
#             end_time = '2017-4-30'
#         data = DevEvent.objects.filter(Q(start_time__gte=start_time) | Q(end_time__lte=end_time)).filter(
#             operator=username).all()
#         query_field = ["work_title", "complete_status"]
#         data_dict = queryset_to_dict(data, query_field)

#         output = StringIO.StringIO()
#         excel_instance = ReportExcel(output)
#         excel_instance.write_excel(data_dict)
#         output.seek(0)

#         response = FileResponse(output.read())
#         response['Content-Type'] = 'application/octet-stream'
#         response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
#             'output.xlsx')
#         return response


class GetWeeklySummary(View):
    '''
    查询所有项目属性
    '''

    def get(self, request):
        getParams = request.GET        
        employee_name= getParams.get('employee_name', '')
        filter_date = getParams.get('filter_date', '')
        if filter_date:
            filter_date='-'.join(getfirstday(filter_date))
        if employee_name:
            user_id=User.objects.get(chinese_name=employee_name).id
        else:
            user_id=0
        data = WeekSummary.objects.filter(summary_owner_id=user_id).all()
        query_field = ["id", "natural_week","summary", "self_evaluation", "plan"]
        data_dict = queryset_to_dict(data, query_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response

class InsertSummary(View):
    def post(self, request):
        user_id=get_user_id(request)        
        data = request.POST

        insert_field = ["natural_week", "summary", "self_evaluation", "plan"]
        result = {}
        for t in insert_field:
            result[t] = data.get(t)

        natural_week=result['natural_week'][:7]
        __match=re.compile('^\d{4}-\d{2}').match(natural_week)
        if __match:
            result['natural_week']=__match.group()
        else:
            return  my_response(code=1, msg=u"自然周填写格式错误", content=content)
        result['summary_owner_id'] = user_id
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
        user_id=get_user_id(request)
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
        where_condition = u'dev.dev_event_owner_id={0} and dev.event_date>="{1}" and dev.event_date<="{2}" '.format(user_id,start_date, end_date)
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

class InsertSaleEvent(View):
    def post(self, request):
        user_id=get_user_id(request)       
        data = request.POST
        print(data)
     
        insert_field = ["visit_date", "cus_con_post", "cus_con_mdn", "cus_con_tel_num", "cus_con_wechart", "communicate_record", "sale_event_remark", "sale_phase_id",
                "active_type_id", "sale_customer_id"]
        result = {}
        for t in insert_field:
            result[t] = data.get(t)

        result['sale_event_owner_id'] = user_id

        content = {"id": 0}
        if result:
            inset_process = SaleEvent(**result)
            inset_process.save()
            try:
                inset_process.save()
                content = {"id": inset_process.id}
                response = my_response(code=0, msg=u"success", content=content)
            except:
                response = my_response(code=1, msg=u"error", content=content)
        return response

class DelSaleEvent(View):
    def post(self, request):
        data = request.POST
        print(data)
        delID = data.get("delID")
        del_event_id = SaleEvent.objects.filter(id=delID).delete()
        print(del_event_id[0])
        if del_event_id[0] == 0:
            response = my_response(code=1, msg=u"删除失败")
        else:
            content = {"id": del_event_id[0]}
            response = my_response(code=0, msg=u"删除成功", content=content)
        return response

class DelSummary(View):
    def post(self, request):
        data = request.POST
        print(data)
        delID = data.get("delID")
        del_event_id = WeekSummary.objects.filter(id=delID).delete()
        print(del_event_id[0])
        if del_event_id[0] == 0:
            response = my_response(code=1, msg=u"删除失败")
        else:
            content = {"id": del_event_id[0]}
            response = my_response(code=0, msg=u"删除成功", content=content)
        return response