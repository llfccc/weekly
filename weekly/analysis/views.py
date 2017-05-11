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
from django.db.models import Q
import StringIO
import pandas as pd
from django.core.cache import cache


class AnanlysisWorker(View):
    '''
    查询每日工作内容
    '''

    def get(self, request):
        getParams = request.GET
        worker_name = getParams.get('worker_name', '')
        filter_date = getParams.get('filterDate', '')
        department_name = getParams.get('department_name', '')
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
        if worker_name:
            where_condition += "and project_name like '%{0}%'".format(project_name)
        if department_name:
            where_condition += "and department_name = '{0}'".format(department_name)

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

        
        if worker_name:
            where_condition += "and project_name like '%{0}%'".format(project_name)
        if department_name:
            where_condition += "and department_name = '{0}'".format(department_name)
        plain_sql = u"SELECT {0} FROM api_devevent as dev left join api_devproject as pro on dev.dev_event_project_id = pro.id \
            left join api_deveventtype on dev.dev_event_type_id = api_deveventtype.id where {1} order by dev.event_date,dev.start_time".format(
            select_param, where_condition)
        print(plain_sql)
        group_sql = u'select event_type_name,count(event_type_name) as event_type_name_count from ({0}) group by event_type_name '.format(plain_sql)
        print(group_sql)
        row = fetch_data(group_sql)

        content = dict_to_json(row)

        response = my_response(code=0, msg=u"查询成功", content=content)
        return response