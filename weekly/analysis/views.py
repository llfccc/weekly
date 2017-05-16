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
        if department_name:
            group_sql = u'select event_type_name,count(event_type_name) as event_type_name_count from ({0}) group by event_type_name '.format(plain_sql)
        if employee_name:
            group_sql = u'select event_type_name,count(event_type_name) as event_type_name_count from ({0}) group by event_type_name '.format(plain_sql)
        if project_name:
            group_sql = u'select event_type_name,count(event_type_name) as event_type_name_count from ({0}) group by event_type_name '.format(plain_sql)
        print(plain_sql)
        row = fetch_data(group_sql)
        #转换数据为echarts能接受的格式
        type_list=[i['event_type_name'] for i in row]
        type_count=[{'name':i['event_type_name'],'value':i['event_type_name_count']} for i in row]

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
        employee_name= getParams.get('employee_name', '')
        project_name = getParams.get('project_name', '')
        department_name = getParams.get('department_name', '')

        # 创建查询条件        
        plain_sql=join_sql(filter_date,project_name,department_name,employee_name)
        #统计分析
        # if department_name:
        #     group_sql = u'select event_type_name,count(event_type_name) as event_type_name_count from ({0}) group by event_type_name '.format(plain_sql)
        # if employee_name:
        #     group_sql = u'select event_type_name,count(event_type_name) as event_type_name_count from ({0}) group by event_type_name '.format(plain_sql)
        # if project_name:
        group_sql = u'select event_type_name,sum(start_time-end_time) as event_type_name_count from ({0}) group by event_type_name '.format(plain_sql)
        #print(plain_sql)
        row = fetch_data(group_sql)
        print(row)
        #转换数据为echarts能接受的格式
        type_list=[i['event_type_name'] for i in row]
        type_count=[{'name':i['event_type_name'],'value':i['event_type_name_count']} for i in row]

        content = dict_to_json({'type_list':type_list,'type_count':type_count})
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response