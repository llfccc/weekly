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
# from django.contrib.auth.decorators import login_required  

from sqljoint.query import filter_dev_event_sql,filter_sale_event_sql
from sqljoint.query import  chinesename_to_userid,userid_to_chinesename

# Create your views here.


class GetDevEvent(View):
    '''
    查询每日工作内容
    '''

    def get(self, request):
        user_id=get_user_id(request)

        print(user_id)
        getParams = request.GET
        project_id = getParams.get('project_name', '')
        filter_date = getParams.get('filter_date', '')
        #没有完成显示出对应的上下游对接人
        # up_user_field=["chinese_name as up_reporter_name "]
        # down_user_field = ["chinese_name as down_reporter_name "]
        plain_sql=filter_dev_event_sql(filter_date,project_id,'','',user_id)

        query_result = fetch_data(plain_sql)
        
        #限定返回给前端的字段
        result_field = ["dev_event_id", "event_date", "project_name", "event_type_name", "description", "start_time","end_time","fin_percentage","dev_event_remark"]
        result_list=[]
        for row in query_result:
            row_dict={}
            #由id转换成对应具体的人名
            row_dict['down_reporter_name']=userid_to_chinesename(row['down_reporter_ids'])
            row_dict['up_reporter_name']=userid_to_chinesename(row['up_reporter_id'])
            for key in result_field:
                row_dict[key]=row.get(key,'')
            result_list.append(row_dict)
        print(result_list)
        content = dict_to_json(result_list)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class GetProjects(View):
    '''
    查询所有项目属性
    '''

    def get(self, request):
        data = DevProject.objects.filter(project_is_closed=False).all()
        result_field = ["id", "creater_id", "status", "dev_project_remark", "project_name", "create_time"]
        data_dict = queryset_to_dict(data, result_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class GetEventTypes(View):
    '''
    查询所有项目属性
    '''

    def get(self, request):
        data = DevEventType.objects.filter(devEventType_is_closed=False).all()
        result_field = ["id", "creator_id", "event_type_name", "dev_event_type_remark", "create_time"]
        data_dict = queryset_to_dict(data, result_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class InsertWork(View):
    '''
    插入工作记录
    '''
    def post(self, request):
        user_id=get_user_id(request)        
        data = request.POST

        insert_field = ["description", "event_date", "start_time", "end_time", "fin_percentage", "up_reporter_id",
                        "down_reporter_ids", "dev_event_remark", "dev_event_project_id", "dev_event_type_id"]

        #查询是否有user_id，如果没有则认为未登录
        content = {"id": 0}    
        result = {}            
        for t in insert_field:
            result[t] = data.get(t,'')

        if user_id!=0:
            result['dev_event_owner_id'] = user_id
        else:
            return my_response(code=1, msg=u"未登录", content=content)

        if result:
            inset_process = DevEvent(**result)
            try:
                inset_process.save()
                content = {"id": inset_process.id}
                response = my_response(code=0, msg=u"success", content=content)
            except:
                response = my_response(code=1, msg=u"插入数据失败", content=content)
        return response


class DelWork(View):
    '''
    删除工作记录
    '''
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
        
        getParams = request.GET
        print(getParams)        
        filter_date = getParams.get('filter_date', '')
        customer_id= getParams.get('customer_id', '')

        #如果传入了周数，则转成日期段
        # if filter_date:
        #     filter_date='-'.join(getfirstday(filter_date))     

        plain_sql=filter_sale_event_sql(filter_date=filter_date,user_id=user_id,customer_id=customer_id)
        row = fetch_data(plain_sql)        
        content = dict_to_json(row)
        print(content)
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

        result_field = ["id", "full_name", "short_name","contact_post", "contact_name", "contact_mdn", "contact_tel_num",
                       "sale_customer_remark", "create_time"]
        data = SaleCustomer.objects.filter(sale_customer_owner_id=user_id).all()
        data_dict = queryset_to_dict(data, result_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response

class GetSaleActiveTypes(View):
    def get(self, request):
        data = SaleActiveType.objects.all()
        result_field = ["id", "active_type_name", "sale_active_type_remark", "create_time"]
        data_dict = queryset_to_dict(data, result_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class GetSalePhases(View):
    def get(self, request):
        data = SalePhase.objects.all()
        result_field = ["id", "phase_name", "description","phase_count","sale_phase_remark" , "create_time"]
        data_dict = queryset_to_dict(data, result_field)
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
#         result_field = ["work_title", "complete_status"]
#         data_dict = queryset_to_dict(data, result_field)

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
        employee_name= getParams.get('employee_name', '').strip()
        filter_date = getParams.get('filter_date', '')
        # department_name =u'销售部'
        #验证日期是否符合 2017-01的格式
        __match=re.compile('^\d{4}-\d{2}').match(filter_date)
        if __match:
            filter_date=__match.group()
        else:
            filter_date=''
        print(filter_date)
        user_id=0

        user_id=chinesename_to_userid(employee_name)
        data = WeekSummary.objects.filter(summary_owner_id=user_id).filter(natural_week=filter_date).all()
        result_field = ["id", "natural_week","summary", "self_evaluation", "plan"]
        data_dict = queryset_to_dict(data, result_field)
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

        delID = data.get("delID")
        del_event_id = WeekSummary.objects.filter(id=delID).delete()
        print(del_event_id[0])
        if del_event_id[0] == 0:
            response = my_response(code=1, msg=u"删除失败")
        else:
            content = {"id": del_event_id[0]}
            response = my_response(code=0, msg=u"删除成功", content=content)
        return response