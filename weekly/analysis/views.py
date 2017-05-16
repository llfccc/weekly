# -*- coding: utf-8 -*-
import os
import json
from django.http import HttpResponse, FileResponse, Http404
import datetime
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