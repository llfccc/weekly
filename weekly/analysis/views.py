# -*- coding: utf-8 -*-
import os
import json
from django.http import HttpResponse, FileResponse, Http404
import datetime
from collections import defaultdict
from django.views.generic import View
from utils.tools import my_response, queryset_to_dict, dict_to_json
from utils.tools import fetch_data
from api.models import DevEvent, DevProject, DevEventType
from api.models import   SaleCustomer, SalePhase, SaleTarget, SaleEvent, SaleActiveType
from api.models import WeekSummary
from accounts.models import User,Department
from django.db.models import Q
import StringIO
import pandas as pd
from django.core.cache import cache
from sqljoint.query import join_sql

class AnanlysisWorker(View):
    '''
    查询职员工作类型占比
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date', '')
        employee_name= getParams.get('employee_name', '')
        project_name = getParams.get('project_name', '')
        department_name = getParams.get('department_name', '')

        # 创建查询条件        
        plain_sql=join_sql(filter_date,project_name,department_name,employee_name)
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
        department_name=u'技术服务中心'
        # 创建查询条件        
        plain_sql=join_sql(filter_date,'',department_name,'','')
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
    查询职员工作类型占比
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date', '')
        project_name = getParams.get('project_name', '')
        department_name=u'技术服务中心'
        # 创建查询条件       
        plain_sql=join_sql(filter_date,project_name,department_name,'','')
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
    查询职员工作类型占比
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date', '')
        department_name=u'技术服务中心'
        # 创建查询条件       
        plain_sql=join_sql(filter_date=filter_date,project_name='',department_name=department_name,employee_name='',user_id='')
        #统计分析select dev_event_project_id, count((end_time-start_time)) as time_diff from api_devevent group by dev_event_project_id
        group_sql = u'select chinese_name, ROUND(sum(extract(EPOCH from child.end_time - child.start_time)/3600/5)::numeric,3)   as date_diff  from ({0}) as child group by chinese_name order by date_diff desc'.format(plain_sql)

        row = fetch_data(group_sql)

        #转换数据为echarts能接受的格式
        x_data=[i['chinese_name'] for i in row]
        y_data=[i['date_diff'] for i in row]

        content = dict_to_json({'x_data':x_data,'y_data':y_data})
    
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response

week_list=['星期日','星期一','星期二','星期三','星期四','星期五','星期六']
class DisplayWeekly(View):
    '''
    查询职员工作类型占比
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date', '')
        employee_name= getParams.get('employee_name', '测试')
        project_name = getParams.get('project_name', '')
        department_name = getParams.get('department_name', '')
        
        # 创建查询条件        
        plain_sql=join_sql(filter_date,project_name,department_name,employee_name)
        #统计分析
        group_sql = u'select event_type_name,ROUND(sum(extract(EPOCH from child.end_time - child.start_time)/3600)::numeric,2) as date_diff from ({0}) as child  group by event_type_name '.format(plain_sql)

        data = fetch_data(plain_sql)

        #先变换数据
        alternation_list=[]
        event_date_list=[]   #保存所有不重复的日期
        for key,value in enumerate(data):           
            event_date=value.get('event_date').strftime("%Y-%m-%d")
            event_date_list.append(event_date)  
            duration_time=((datetime.datetime.combine(datetime.date.today(), value['end_time']) - datetime.datetime.combine(datetime.date.today(), value['start_time'],)).total_seconds()/60)
            data_list=['project_name','event_type_name','description','up_reporter_id','down_reporter_ids','fin_percentage','dev_event_remark']
            field_data={key:value.get(key) for key in data_list}
            field_data['duration_time']=duration_time
            field_data['event_date']=event_date
            alternation_list.append(field_data)

        event_date_list=set(event_date_list)
        result=dict.fromkeys(event_date_list)
        for value in alternation_list:
            if not result[value['event_date']]:
                #初始化时间合计
                result[value['event_date']]={'total_time':value['duration_time']}
                result[value['event_date']]['other_row']=[]
                #计算周几
                date=datetime.datetime.strptime(value['event_date'],"%Y-%m-%d")
                week_id=int(date.strftime("%w"))
                which_day=week_list[week_id]  
                result[value['event_date']]['which_day']=which_day
            if result[value['event_date']] and 'total_time' in result[value['event_date']]:            
                result[value['event_date']]['total_time']+=value['duration_time']
            result[value['event_date']]['other_row'].append(value)

        finalResult=[]
        for index,value in enumerate(event_date_list):
            finalResult.append({'event_date':value,'total_time':result[value]['total_time'],'which_day':result[value]['which_day'],'other_row':result[value]['other_row']})
       
        content = dict_to_json(finalResult)
        #转换数据为echarts能接受的格式
        # type_list=[i['event_type_name'] for i in row]
        # type_count=[{'name':i['event_type_name'],'value':i['date_diff']} for i in row]

        # content = dict_to_json({'type_list':type_list,'type_count':type_count})
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response