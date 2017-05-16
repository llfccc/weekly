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


def join_sql(filter_date='',project_name='',department_name='',employee_name='',user_id=''):
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
        department_id=Department.objects.get(department_name=department_name).id 
        user_queryset=User.objects.filter(department_id=department_id).all()
        user_ids=tuple([i.id for i in user_queryset])           
        if user_ids:
            #如果user_ids只有1个数，则python会因为元祖在后面加一个“，”，导致sql无法执行
            if len(user_ids)==1:
                where_condition += "and dev_event_owner_id =  '{0}' ".format(user_ids[0])
            else:
                where_condition += "and dev_event_owner_id in  {0} ".format(user_ids)

    if employee_name:       
        user_id=User.objects.get(chinese_name=employee_name).id     
        where_condition += "and dev_event_owner_id = '{0}' ".format(user_id)
    if user_id:     
        where_condition += "and dev_event_owner_id = '{0}' ".format(user_id)

    plain_sql = u"SELECT {0} FROM api_devevent as dev left join api_devproject as pro on dev.dev_event_project_id = pro.id \
        left join api_deveventtype on dev.dev_event_type_id = api_deveventtype.id \
        left join accounts_user  on accounts_user.id = dev.dev_event_owner_id \
        where {1} order by dev.event_date,dev.start_time".format(
        select_param, where_condition)        
    return plain_sql