# -*- coding: utf-8 -*-
from utils.tools import getMondaySunday
from accounts.models import User,Department

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


def filter_dev_event_sql(filter_date='',project_name='',department_name='',employee_name='',user_id=''):
    '''
    给sql加入筛选条件
    '''
    select_param="*,dev.id as dev_event_id" 
    
    start_date, end_date=default_date(filter_date)
    where_condition = u"dev.event_date>='{0}' and dev.event_date<='{1}' ".format(start_date, end_date)
    if project_name:
        where_condition += "and project_name like '%{0}%' ".format(project_name)
    #筛选部门中所有人员
    if department_name:        
        department_queryset=Department.objects.filter(department_name=department_name)
        if department_queryset:
            department_id=department_queryset.first().id
        else:
            department_id=0
        user_queryset=User.objects.filter(department_id=department_id).all()
        user_ids=tuple([i.id for i in user_queryset])           
        if user_ids:
            #如果user_ids只有1个数，则python会因为元祖在后面加一个“，”，导致sql无法执行
            if len(user_ids)==1:
                where_condition += "and dev_event_owner_id =  {0} ".format(user_ids[0])
            else:
                where_condition += "and dev_event_owner_id in  {0} ".format(user_ids)

    #筛选记录所属人
    if user_id:     
        where_condition += "and dev_event_owner_id = '{0}' ".format(user_id)
    else:
        if employee_name:       
            user_queryset=User.objects.filter(chinese_name=employee_name)
            if user_queryset:
                user_id=user_queryset.first().id
            else:
                user_id=0     
            where_condition += "and dev_event_owner_id = '{0}' ".format(user_id)

    plain_sql = u"SELECT {0} FROM api_devevent as dev left join api_devproject as pro on dev.dev_event_project_id = pro.id \
        left join api_deveventtype on dev.dev_event_type_id = api_deveventtype.id \
        left join accounts_user  on accounts_user.id = dev.dev_event_owner_id \
        where {1} order by dev.event_date,dev.start_time".format(
        select_param, where_condition)        
    return plain_sql

def filter_sale_event_sql(filter_date='', employee_name='',department_name='',user_id=''):
    '''
    给sql加入筛选条件
    '''

    sale_event_field = ["sale.id as sale_event_id", "cus_con_post", "visit_date", "cus_con_mdn", "cus_con_tel_num", "cus_con_wechart", "communicate_record", "sale_event_remark"]
    active_type_field=['active_type_name']
    sale_customer_field=['short_name']
    sale_phase_field=['phase_name']
    user_field=['chinese_name','accounts_user.id as user_id']
    all_select_field = sale_event_field + active_type_field + sale_customer_field+sale_phase_field+user_field
    select_param = ",".join(all_select_field)

    start_date, end_date=default_date(filter_date)
    where_condition = u"sale.visit_date>='{0}' and sale.visit_date<='{1}' ".format(start_date, end_date)

    #筛选记录所属人
    if user_id:     
        where_condition += "and sale_event_owner_id = '{0}' ".format(user_id)
    else:
        if employee_name:       
            user_queryset=User.objects.filter(chinese_name=employee_name)
            if user_queryset:
                user_id=user_queryset.first().id     
            where_condition += "and sale_event_owner_id = '{0}' ".format(user_id)

    plain_sql = u"SELECT {0} FROM api_saleevent as sale\
        left join api_saleactivetype as type on sale.active_type_id = type.id \
        left join api_salecustomer as customer on sale.sale_customer_id = customer.id \
        left join api_salephase as phase on sale.sale_phase_id = phase.id \
        left join accounts_user  on accounts_user.id = sale.sale_event_owner_id \
        where {1} ".format(select_param,where_condition)

    return plain_sql