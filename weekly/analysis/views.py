# -*- coding: utf-8 -*-
import os
import json
import re
import StringIO
import pandas as pd
import datetime
from collections import defaultdict
from django.views.generic import View
from django.db.models import Q
from django.http import HttpResponse, FileResponse, Http404
from django.core.cache import cache
from api.models import DevEvent, DevProject, DevEventType
from api.models import   SaleCustomer, SalePhase, SaleTarget, SaleEvent, SaleActiveType
from api.models import WeekSummary
from accounts.models import User,Department
from utils.tools import my_response, queryset_to_dict, dict_to_json
from utils.tools import fetch_data,getfirstday,day_of_week
from sqljoint.query import filter_dev_event_sql,filter_sale_event_sql,pivot_target_actual_sql
from sqljoint.query import  chinesename_to_userid,userid_to_chinesename
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin


class AnanlysisWorker(View):
    '''
    查询职员工作类型占比
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date', '')
        employee_name= getParams.get('employee_name', '')
        # department_name= getParams.get('department_name', '')
        if not employee_name:
            employee_name=u'空姓名'
        #error
        department_name=u'技术服务中心'
        # 创建查询条件        
        plain_sql=filter_dev_event_sql(filter_date=filter_date,employee_name=employee_name,project_id='',project_name='',department_name='',user_id='')
        #统计分析
        group_sql = u'select event_type_name,ROUND(sum(extract(EPOCH from child.end_time - child.start_time)/3600)::numeric,2) as date_diff from ({0}) as child  group by event_type_name '.format(plain_sql)

        row = fetch_data(group_sql)
        #转换数据为echarts能接受的格式
        type_list=[i['event_type_name'] for i in row]
        type_count=[{'name':i['event_type_name'],'value':i['date_diff']} for i in row]

        content = dict_to_json({'type_list':type_list,'type_count':type_count})
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class AnanlysisDepartment(View):
    '''
    查询职员工作类型占比
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date', '')
        department_name = request.user.department.department_name
        if not department_name:
            department_name=u"空部门"
        # 创建查询条件        
        plain_sql=filter_dev_event_sql(filter_date=filter_date,project_id='',project_name='',department_name=department_name,employee_name='',user_id='')
        #统计分析
        group_sql = u'select event_type_name,ROUND(sum(extract(EPOCH from child.end_time - child.start_time)/3600)::numeric,2) as date_diff from ({0}) as child  group by event_type_name '.format(plain_sql)
        row = fetch_data(group_sql)
        #转换数据为echarts能接受的格式
        type_list=[i['event_type_name'] for i in row]
        type_count=[{'name':i['event_type_name'],'value':i['date_diff']} for i in row]

        content = dict_to_json({'type_list':type_list,'type_count':type_count})
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response

class AnanlysisProject(View):
    '''
    查询某项目工作耗时占比
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date', '')
        project_name = getParams.get('project_name', '')

        department_name = request.user.department.department_name
        if  not project_name:
            project_name=-1

        # 创建查询条件       
        plain_sql=filter_dev_event_sql(filter_date=filter_date,project_name=project_name,project_id='',department_name=department_name)
        #统计分析select dev_event_project_id, count((end_time-start_time)) as time_diff from api_devevent group by dev_event_project_id
        group_sql = u'select chinese_name,ROUND(sum(extract(EPOCH from child.end_time - child.start_time)/3600)::numeric,2)   as date_diff from ({0})  as child group by chinese_name order by date_diff desc '.format(plain_sql)

        row = fetch_data(group_sql)

        #转换数据为echarts能接受的格式
        x_data=[i['chinese_name'] for i in row]
        y_data=[i['date_diff'] for i in row] 
        content = dict_to_json({'x_data':x_data,'y_data':y_data})    
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class AnanlysisLoad(View):
    '''
    查询整个部门职员工作类型占比
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date','')
        department_name = request.user.department.department_name
  
        # 创建查询条件       
        plain_sql=filter_dev_event_sql(filter_date=filter_date,project_id='',project_name='',department_name=department_name,employee_name='',user_id='')
        group_sql = u'select chinese_name, ROUND(sum(extract(EPOCH from child.end_time - child.start_time)/3600/5)::numeric,3)   as date_diff  from ({0}) as child group by chinese_name order by date_diff desc'.format(plain_sql)

        row = fetch_data(group_sql)
     

        #转换数据为echarts能接受的格式
        x_data=[i['chinese_name'] for i in row]
        y_data=[i['date_diff'] for i in row]

        content = dict_to_json({'x_data':x_data,'y_data':y_data})
    
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class AnalysisDevEvent(View):
    '''
    查询非销售职员工每日工作事件
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date', '')
        employee_name= getParams.get('employee_name', '')

        department_name = request.user.department.department_name

        if filter_date:
            filter_date='-'.join(getfirstday(filter_date))
        # 创建查询条件
        if employee_name:          
            plain_sql=filter_dev_event_sql(filter_date=filter_date,project_id='',department_name=department_name,employee_name=employee_name)
        else:
            return  my_response(code=1, msg=u"缺少雇员姓名条件")
         
        #统计分析
        group_sql = u'select event_type_name,ROUND(sum(extract(EPOCH from child.end_time - child.start_time)/3600)::numeric,2) as date_diff from ({0}) as child  group by event_type_name '.format(plain_sql)

        data = fetch_data(plain_sql)
        #先变换数据
        alternation_list=[]
        event_date_list=[]   #保存所有不重复的日期
        for key,value in enumerate(data): 
            '''
            获取所有日期字段保存为list，并将需要的字段放入alternation_list备用
            '''          
            event_date=value.get('event_date').strftime("%Y-%m-%d")
            event_date_list.append(event_date)  
            duration_time=((datetime.datetime.combine(datetime.date.today(), value['end_time']) - datetime.datetime.combine(datetime.date.today(), value['start_time'],)).total_seconds()/60)
            data_list=['project_name','event_type_name','description','up_reporter_id','down_reporter_ids','fin_percentage','dev_event_remark']
            field_data={key:value.get(key) for key in data_list}
            field_data['duration_time']=int(duration_time)
            field_data['event_date']=event_date
            field_data['up_reporter_name']=userid_to_chinesename(value.get('up_reporter_id'))
            field_data['down_reporter_name']=userid_to_chinesename(value.get('down_reporter_ids'))
            alternation_list.append(field_data)

        event_date_list=list(set(event_date_list))      
        event_date_list.sort(reverse=True)

        result=dict.fromkeys(event_date_list)
        for value in alternation_list:
            '''
            统计每天的耗时
            '''
            if not result[value['event_date']]:
                #初始化时间合计
                result[value['event_date']]={'total_time':0}
                result[value['event_date']]['other_row']=[]
                #计算周几
                result[value['event_date']]['which_day']= day_of_week(value['event_date']) 
            if result[value['event_date']] and 'total_time' in result[value['event_date']]:            
                result[value['event_date']]['total_time']+=value['duration_time']
            result[value['event_date']]['other_row'].append(value)

        finalResult=[]
        for index,value in enumerate(event_date_list):
            finalResult.append({'event_date':value,'total_time':round(result[value]['total_time'],2),'which_day':result[value]['which_day'],'other_row':result[value]['other_row']})
       
        content = dict_to_json(finalResult)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response

class DisplaySaleEvent(View):
    '''
    主管查询销售周报汇总
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date', '')
        employee_name= getParams.get('employee_name', '')
        # project_name = getParams.get('project_name', '')
        department_name = request.user.department.department_name
        if filter_date:
            filter_date='-'.join(getfirstday(filter_date))
        # print(filter_date)
        # 创建查询条件        
        plain_sql=filter_sale_event_sql(filter_date=filter_date,employee_name=employee_name,department_name='')
        #统计分析
        # group_sql = u'select event_type_name,ROUND(sum(extract(EPOCH from child.end_time - child.start_time)/3600)::numeric,2) as date_diff from ({0}) as child  group by event_type_name '.format(plain_sql)

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

class AnalysisSalePerformace(View):
    '''
    查询销售职员工作类型占比
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date', '')
        department_name = request.user.department.department_name
  
        natural_week=''
        if filter_date:
            natural_week = filter_date[:7]
            filter_date='-'.join(getfirstday(filter_date))
        filter_sql=filter_sale_event_sql(filter_date=filter_date,department_name=department_name)
        # 联合目标和实际记录
        pivot_sql=pivot_target_actual_sql(natural_week=natural_week,filter_sql=filter_sql,department_name=department_name)
        
        data = fetch_data(pivot_sql)
        content = dict_to_json(data)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class AnalysisWeeklySummary(LoginRequiredMixin,View):
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
            filter_date='2017-21'

        user_id=chinesename_to_userid(employee_name)
        data = WeekSummary.objects.filter(summary_owner_id=user_id).filter(natural_week=filter_date).all()
        result_field = ["id", "natural_week","summary", "self_evaluation", "plan"]
        data_dict = queryset_to_dict(data, result_field)
        content = dict_to_json(data_dict)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response