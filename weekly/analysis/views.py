# -*- coding: utf-8 -*-
import os
import json
from django.http import HttpResponse, FileResponse, Http404
import datetime
from collections import defaultdict
from django.views.generic import View
from utils.tools import my_response, queryset_to_dict, dict_to_json
from utils.tools import fetch_data,getfirstday,day_of_week
from api.models import DevEvent, DevProject, DevEventType
from api.models import   SaleCustomer, SalePhase, SaleTarget, SaleEvent, SaleActiveType
from api.models import WeekSummary
from accounts.models import User,Department
from django.db.models import Q
import StringIO
import pandas as pd
from django.core.cache import cache
from sqljoint.query import filter_dev_event_sql,filter_sale_event_sql
from sqljoint.query import  chinesename_to_userid,userid_to_chinesename

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
        plain_sql=filter_dev_event_sql(filter_date,project_name,department_name,employee_name)
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
        plain_sql=filter_dev_event_sql(filter_date,'',department_name,'','')
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
        plain_sql=filter_dev_event_sql(filter_date,project_name,department_name,'','')
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
        plain_sql=filter_dev_event_sql(filter_date=filter_date,project_name='',department_name=department_name,employee_name='',user_id='')
        #统计分析select dev_event_project_id, count((end_time-start_time)) as time_diff from api_devevent group by dev_event_project_id
        group_sql = u'select chinese_name, ROUND(sum(extract(EPOCH from child.end_time - child.start_time)/3600/5)::numeric,3)   as date_diff  from ({0}) as child group by chinese_name order by date_diff desc'.format(plain_sql)

        row = fetch_data(group_sql)

        #转换数据为echarts能接受的格式
        x_data=[i['chinese_name'] for i in row]
        y_data=[i['date_diff'] for i in row]

        content = dict_to_json({'x_data':x_data,'y_data':y_data})
    
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


class DisplayWeekly(View):
    '''
    查询职员工每日工作事件
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date', '')
        employee_name= getParams.get('employee_name', '')
        project_id = getParams.get('project_id', '')
        #error，此处需要修改强制条件为主管所属部门
        department_name = getParams.get('department_name', '销售部')
        
        if filter_date:
            filter_date='-'.join(getfirstday(filter_date))
  
        # 创建查询条件
        if employee_name:          
            plain_sql=filter_dev_event_sql(filter_date=filter_date,project_id=project_id,department_name=department_name,employee_name=employee_name)
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
            field_data['duration_time']=duration_time
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
                result[value['event_date']]={'total_time':value['duration_time']}
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
    查询销售周报
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date', '')
        employee_name= getParams.get('employee_name', '')
        # project_name = getParams.get('project_name', '')
        department_name = getParams.get('department_name', '')
        
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
            result_dict['which_day']=day_of_week(row['visit_date'])
            result_list.append(result_dict)

        content = dict_to_json(result_list)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response

class GetSalePerformace(View):
    '''
    查询职员工作类型占比
    '''

    def get(self, request):
        getParams = request.GET        
        filter_date = getParams.get('filter_date', '')
        # employee_name= getParams.get('employee_name', '')
        # project_name = getParams.get('project_name', '')
        department_name = getParams.get('department_name', '')
        
        natural_week=''
        if filter_date:
            natural_week = filter_date[:7]
            filter_date='-'.join(getfirstday(filter_date))

        target_sql=u"select sale_target_owner_id,phase_name as target_phase_name,target from api_saletarget where natural_week='{0}'".format(natural_week)
        # 创建查询条件        
        # employee_filter={'employee_name':employee_name}
        plain_sql=filter_sale_event_sql(filter_date=filter_date,department_name=department_name)

        #统计分析
        group_sql = u'select child.user_id,child.chinese_name,child.phase_name,count(child.phase_name) as phase_count \
            from ({0}) as child group by child.phase_name,child.chinese_name,child.user_id '.format(plain_sql)

        # join_sql=u''
        union_sql=u'''select  a_user.chinese_name,phase_name,phase_count,target_phase_name,target \
                    from ({1}) as target  \
                    left join ({0}) as group_count on \
                    target.sale_target_owner_id=group_count.user_id and target.target_phase_name=group_count.phase_name
                    left join accounts_user as a_user on  target.sale_target_owner_id=a_user.id'''.format(group_sql,target_sql)
        pivot_sql=u'''select chinese_name,   
            sum(case when phase_name = 'A' then phase_count else 0 end) as "A",  
            sum(case when phase_name = 'B' then phase_count else 0 end) as "B",  
            sum(case when phase_name = 'C' then phase_count else 0 end) as "C",
            sum(case when phase_name = 'D' then phase_count else 0 end) as "D",
            sum(case when phase_name = 'E' then phase_count else 0 end) as "E",
            sum(case when phase_name = 'F' then phase_count else 0 end) as "F",
            sum(case when target_phase_name = 'A' then target else 0 end) as "target_A",  
            sum(case when target_phase_name = 'B' then target else 0 end) as "target_B",  
            sum(case when target_phase_name = 'C' then target else 0 end) as "target_C",
            sum(case when target_phase_name = 'D' then target else 0 end) as "target_D",
            sum(case when target_phase_name = 'E' then target else 0 end) as "target_E",
            sum(case when target_phase_name = 'F' then target else 0 end) as "target_F"       
            from  ({0}) as group_sql group by chinese_name order by chinese_name desc;  '''.format(union_sql)
        print(pivot_sql)
        data = fetch_data(pivot_sql)
        content = dict_to_json(data)
        # print(content)
        response = my_response(code=0, msg=u"查询成功", content=content)
        return response


