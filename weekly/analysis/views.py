# -*- coding: utf-8 -*-
import os
import json
from django.http import HttpResponse, FileResponse, Http404
import datetime
from django.views.generic import View
from utils.tools import my_response, queryset_to_dict, dict_to_json, getMondaySunday
from utils.tools import fetch_data
from api.models import DevEvent, DevProject, DevEventType
from api.models import   SaleCustomer, SalePhase, SaleTarget, SaleEvent, SaleActiveType
from api.models import WeekSummary
from accounts.models import User,Department
from django.db.models import Q
import StringIO
import pandas as pd
from django.core.cache import cache


def default_date(filter_date):
    if filter_date:
        try:
            start_date = filter_date[:10]
            end_date = filter_date[13:]
        except:
            start_date, end_date = getMondaySunday()
    else:
        start_date, end_date = getMondaySunday()
    return (start_date,end_date)


def join_sql(filter_date='',project_name='',department_name='',employee_name=''):
    
        select_param="*,dev.id as dev_event_id"
        
        start_date, end_date=default_date(filter_date)
        where_condition = u'dev.event_date>="{0}" and dev.event_date<="{1}" '.format(start_date, end_date)
        if project_name:
            where_condition += "and project_name like '%{0}%'".format(project_name)
        #筛选部门中所有人员
        if department_name:
            department_id=Department.objects.get(department_name=department_name).id 
            user_queryset=User.objects.filter(department_id=department_id).all()
            user_ids=tuple([i.id for i in user_queryset])           
            if user_ids:
                #如果user_ids只有1个数，则python会因为元祖在后面加一个“，”，导致sql无法执行
                if len(user_ids)==1:
                    where_condition += "and dev_event_owner_id =  '{0}'".format(user_ids[0])
                else:
                    where_condition += "and dev_event_owner_id in  {0}".format(user_ids)

        if employee_name:       
            user_id=User.objects.get(chinese_name=employee_name).id     
            where_condition += "and dev_event_owner_id = '{0}'".format(user_id)

        plain_sql = u"SELECT {0} FROM api_devevent as dev left join api_devproject as pro on dev.dev_event_project_id = pro.id \
            left join api_deveventtype on dev.dev_event_type_id = api_deveventtype.id where {1} order by dev.event_date,dev.start_time".format(
            select_param, where_condition)        
        #print(plain_sql)
        return plain_sql

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