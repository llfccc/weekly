# coding:utf-8
import os
import json
import re
import StringIO
import pandas as pd
import datetime

from django.views.generic import View
from django.http import HttpResponse, FileResponse, Http404
from .models import DevEvent, DevProject, DevEventType
from .models import   SaleCustomer, SalePhase, SaleTarget, SaleEvent, SaleActiveType
from .models import WeekSummary
from django.db.models import Q
from django.core.cache import cache
from django.db import connection, transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
# from django.contrib.auth.decorators import login_required  
from utils.tools import my_response, queryset_to_dict, dict_to_json
from utils.export_excel import ReportExcel
from utils.tools import fetch_data,get_user_id,get_first_day,get_day_of_week
from sqljoint.query import filter_dev_event_sql,filter_sale_event_sql
from sqljoint.query import  chinesename_to_userid,userid_to_chinesename
from utils.tools import fetch_data,get_first_day,day_of_week



# Create your views here.
# def email_check(request):
#     return request.user.email.endswith('@live.cn')

class GetDevEvent(LoginRequiredMixin,View):
    '''
    查询自己填写的每日工作内容
    '''
    # @user_passes_test(email_check)
    def get(self, request):
        user_id=get_user_id(request)

        getParams = request.GET
        project_id = getParams.get('project_id', '')
        filter_date = getParams.get('filter_date', '')
        natural_week = getParams.get('natural_week', '')
        plain_sql=filter_dev_event_sql(filter_date=filter_date,natural_week=natural_week,project_id=project_id,user_id=user_id)
        query_result = fetch_data(plain_sql)

        #限定返回给前端的字段
        # result_field = [, "event_date", "project_name", "event_type_name", "description", "start_time","end_time","fin_percentage","dev_event_remark"]

        alternation_list=[]
        event_date_list=[]   #保存所有不重复的日期
        for key,value in enumerate(query_result): 
            '''
            获取所有日期字段保存为list，并将需要的字段放入alternation_list备用
            '''          
            event_date=value.get('event_date').strftime("%Y-%m-%d")
            event_date_list.append(event_date)  
            duration_time=((datetime.datetime.combine(datetime.date.today(), value['end_time']) - datetime.datetime.combine(datetime.date.today(), value['start_time'],)).total_seconds()/60)
            data_list=["dev_event_id",'project_name',"start_time","end_time",'event_type_name','description','up_reporter_id','down_reporter_ids','fin_percentage','dev_event_remark']
            field_data={key:value.get(key) for key in data_list}
            field_data['duration_time']=int(duration_time)
            field_data['event_date']=event_date
            field_data['which_day']=day_of_week(field_data['event_date']) 
            field_data['up_reporter_name']=userid_to_chinesename(value.get('up_reporter_id'))
            field_data['down_reporter_name']=userid_to_chinesename(value.get('down_reporter_ids'))
            alternation_list.append(field_data)
        content = dict_to_json(alternation_list)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class GetProjects(LoginRequiredMixin,View):
    '''
    查询所有项目属性
    '''

    def get(self, request):
        data = DevProject.objects.filter(closed_status=0).all()
        result_field = ["id", "creater_id", "status", "dev_project_remark", "project_name", "create_time"]
        data_dict = queryset_to_dict(data, result_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class GetEventTypes(LoginRequiredMixin,View):
    '''
    查询所有项目属性
    '''

    def get(self, request):
        data = DevEventType.objects.filter(closed_status=0).all()
        result_field = ["id", "creator_id", "event_type_name", "dev_event_type_remark", "create_time"]
        data_dict = queryset_to_dict(data, result_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class InsertDevWork(LoginRequiredMixin,View):
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
            field_value=data.get(t,None)
            if field_value:
                result[t] = field_value.strip()

        if result['fin_percentage'].isdigit():
            if not (int(result['fin_percentage'])>0 and int(result['fin_percentage'])<=100):
                return my_response(code=1, msg=u"数字范围取值错误", content=content)
        else:
            return my_response(code=1, msg=u"百分比需要填写数字", content=content)
        result['dev_event_owner_id'] = user_id

        try:
            insert_process = DevEvent(**result)
            insert_process.save()
            content = {"id": insert_process.id}
            response = my_response(code=0, msg=u"success", content=content)
        except:
            response = my_response(code=1, msg=u"插入数据失败", content=content)
        return response


class Test(LoginRequiredMixin,View):
    def get(self, request):
        print(request.user)
        print request.user.get_all_permissions()
        if request.user.has_perm('api.view_devproject'):
            print("yese")
        return HttpResponse(request.user.get_all_permissions())


class GetSaleEvents(LoginRequiredMixin,View):
    ''''
    查询个人拜访记录
    '''

    def get(self, request):
        user_id=get_user_id(request)        
        getParams = request.GET
       
        filter_date = getParams.get('filter_date','')
        customer_id= getParams.get('customer_id', '')
        natural_week = getParams.get('natural_week', '')
        #如果传入了周数，则转成日期段
        # if filter_date:
        #     filter_date='-'.join(getfirstday(filter_date))

        plain_sql=filter_sale_event_sql(filter_date=filter_date,natural_week=natural_week,user_id=user_id,customer_id=customer_id,department_name='')
        data = fetch_data(plain_sql)
        result_list=[]
        for row in data:
            result_dict={}
            for key,value in row.items():
                result_dict[key]=value
            result_dict['which_day']=day_of_week(str(row['visit_date']))
            result_list.append(result_dict)     
        content = dict_to_json(result_list)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response

class InsertCustomer(LoginRequiredMixin,View):
    def post(self, request):
        user_id=get_user_id(request)
        content = {"id": 0}
        data = request.POST
        insert_field = ["full_name", "short_name","contact_post", "contact_name", "contact_mdn", "contact_tel_num",
                       "sale_customer_remark"]
        result = {}
        for t in insert_field:
            field_value=data.get(t,None)
            if field_value:
                result[t] = field_value.strip()

        customer_exist=SaleCustomer.objects.filter(full_name=result.get('full_name')).all()
        if customer_exist:
            return my_response(code=1, msg=u"客户已存在")             
        result['sale_customer_owner_id'] = user_id        

        if result:
            insert_process = SaleCustomer(**result)
            try:
                insert_process.save()
                content = {"id": insert_process.id}

                response = my_response(code=0, msg=u'恭喜你，新增成功', content=content)
            except:
                response = my_response(code=1, msg=u'插入失败', content=content)
        return response

class GetCustomers(LoginRequiredMixin,View):
    def get(self, request):
        user_id=get_user_id(request)

        result_field = ["id", "full_name", "short_name","contact_post", "contact_name", "contact_mdn", "contact_tel_num",
                       "sale_customer_remark", "create_time"]
        data = SaleCustomer.objects.filter(sale_customer_owner_id=user_id).all()
        data_dict = queryset_to_dict(data, result_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response

class GetSaleActiveTypes(LoginRequiredMixin,View):
    def get(self, request):
        data = SaleActiveType.objects.filter(closed_status=0).all()
        result_field = ["id", "active_type_name", "sale_active_type_remark", "create_time"]
        data_dict = queryset_to_dict(data, result_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class GetSalePhases(LoginRequiredMixin,View):
    def get(self, request):
        data = SalePhase.objects.filter(closed_status=0).all()
        result_field = ["id", "phase_name", "description","phase_count","sale_phase_remark" , "create_time"]
        data_dict = queryset_to_dict(data, result_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


# class GetExcel(LoginRequiredMixin,View):
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


class GetWeeklySummary(LoginRequiredMixin,View):
    '''
    员工查询自己的周总结
    '''

    def get(self, request):
        getParams = request.GET        
        # employee_name= getParams.get('employee_name', '').strip()
        natural_week = getParams.get('natural_week', '')
        # department_name =u'销售部'
        #验证日期是否符合 2017-01的格式
        __match=re.compile('^\d{4}-\d{2}').match(natural_week)
        if __match:
            natural_week=__match.group()
        else:
            natural_week= get_day_of_week()

        user_id=get_user_id(request)

        data = WeekSummary.objects.filter(summary_owner=user_id).filter(natural_week=natural_week).all()

        result_field = ["id", "natural_week","summary", "self_evaluation", "plan"]
        data_dict = queryset_to_dict(data, result_field)
        content = dict_to_json(data_dict)
   
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response

class InsertSummary(LoginRequiredMixin,View):
    def post(self, request):
        user_id=get_user_id(request)        
        data = request.POST

        insert_field = ["natural_week", "summary", "self_evaluation", "plan"]
        result = {}
        for t in insert_field:
            result[t] = data.get(t,None).strip()

        natural_week=result['natural_week'][:7]
        __match=re.compile('^\d{4}-\d{2}').match(natural_week)

        if __match:
            result['natural_week']=__match.group()
        else:
            return  my_response(code=1, msg=u"自然周填写格式错误", content='')
        result['summary_owner_id'] = user_id
        

        if result:
            content = {"id": 0}
            insert_process = WeekSummary(**result)
            try:
                insert_process.save()
                content = {"id": insert_process.id}
                response = my_response(code=0, msg=u"插入成功", content=content)
            except:
                response = my_response(code=1, msg=u"插入失败", content=content)
        return response

class GetEventExcel(LoginRequiredMixin,View):
    '''
    查询每日工作内容,并导出为excel
    '''

    def get(self, request):
        user_id=get_user_id(request)
        getParams = request.GET
        project_id = getParams.get('project_id', '')
        filter_date = getParams.get('filter_date', '')
        natural_week = getParams.get('natural_week', '')
        plain_sql=filter_dev_event_sql(filter_date=filter_date,natural_week=natural_week,project_id=project_id,user_id=user_id)
        query_result = fetch_data(plain_sql)
        
        #限定返回给前端的字段
        result_field = ["dev_event_id", "event_date", "project_name", "event_type_name", "description", "fin_percentage","dev_event_remark"]
        result_list=[]
        for row in query_result:
            row_dict={}
            #由id转换成对应具体的人名
            row_dict['down_reporter_name']=userid_to_chinesename(row.get('down_reporter_ids'))
            row_dict['up_reporter_name']=userid_to_chinesename(row.get('up_reporter_id'))
            row_dict['duration_time']=((datetime.datetime.combine(datetime.date.today(), row.get('end_time')) - datetime.datetime.combine(datetime.date.today(), row.get('start_time'), )).total_seconds() / 60)

            for key in result_field:
                row_dict[key]=row.get(key,'')
            result_list.append(row_dict)
        # Create a Pandas dataframe from the data.
        df = pd.DataFrame.from_dict(result_list)
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
            u'导出.xlsx')
        return response

class InsertSaleEvent(LoginRequiredMixin,View):
    def post(self, request):
        user_id=get_user_id(request)       
        data = request.POST
        
        insert_field = ["visit_date", "cus_con_post", "cus_con_mdn", "cus_con_tel_num", "cus_con_wechart", "communicate_record", "sale_event_remark", "sale_phase_id",
                "active_type_id", "sale_customer_id"]
        result = {}
        for t in insert_field:
            field_value=data.get(t,None)
            if field_value:
                result[t] = field_value.strip()

        result['sale_event_owner_id'] = user_id
        content = {"id": 0}

        if result:
            insert_process = SaleEvent(**result) 
            try:
                insert_process.save()
                content = {"id": insert_process.id}
                response = my_response(code=0, msg=u"新增拜访记录成功", content=content)
            except:
                response = my_response(code=1, msg=u"新增失败，可能漏填项目", content=content)
        return response



class DelDevEvent(LoginRequiredMixin,View):
    '''
    删除员工自己的工作记录 LoginRequiredMixin,
    '''

    def get(self, request):
        user_id=get_user_id(request) 
        data = request.GET
        delID = data.get("delID",-1)
        del_queryset = DevEvent.objects.filter(id=delID).first()
        if not del_queryset:
            return  my_response(code=1, msg=u"删除失败，可能已经不存在")
        if  del_queryset.dev_event_owner_id==user_id:
            deleted_id=del_queryset.delete()
            content = {"id": deleted_id}
            response = my_response(code=0, msg=u"删除成功", content=content)
        else:
            response = my_response(code=1, msg=u"你不是该记录的所有人")
        return response


class DelSaleEvent(LoginRequiredMixin,View):
    '''
    员工删除自己的拜访记录
    '''
    def get(self, request):
        user_id=get_user_id(request) 
        data = request.GET
        delID = data.get("delID",-1)
        del_queryset = SaleEvent.objects.filter(id=delID).first()
        if not del_queryset:
            return  my_response(code=1, msg=u"删除失败，可能已经不存在")
        if  del_queryset.sale_event_owner_id==user_id:
            deleted_id=del_queryset.delete()
            content = {"id": deleted_id}
            response = my_response(code=0, msg=u"删除成功", content=content)
        else:
            response = my_response(code=1, msg=u"你不是该记录的所有人")
        return response

class DelSummary(LoginRequiredMixin,View):
    '''
    删除个人总结
    '''
    def get(self, request):
        user_id=get_user_id(request) 
        data = request.GET
        delID = data.get("delID",-1)
        del_queryset = WeekSummary.objects.filter(id=delID).first()
        if not del_queryset:
            return  my_response(code=1, msg=u"删除失败，可能已经不存在")
        if  del_queryset.summary_owner_id==user_id:
            deleted_id=del_queryset.delete()
            content = {"id": deleted_id}
            response = my_response(code=0, msg=u"删除成功", content=content)
        else:
            response = my_response(code=1, msg=u"你不是该记录的所有人")
        return response