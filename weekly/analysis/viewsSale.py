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
    主管查询销售职员目标与实际情况
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
        print(data)
        print len(data)
        content = dict_to_json(data)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


