# -*- coding: utf-8 -*-
from utils.tools import getMondaySunday,get_first_day
from accounts.models import User,Department

def default_date(filter_date):
    '''
    如果传入日期为空，则返回当周默认第一天和最后一天。如果传入“2017-05-11-2017-06-22”否则返回拆开后的日期
    '''
    if filter_date:
        try:
            start_date = filter_date[:10]
            end_date = filter_date[13:]
        except:
            start_date, end_date = getMondaySunday()
    else:
        start_date, end_date = getMondaySunday()
    return (start_date,end_date)


def filter_dev_event_sql(filter_date='',natural_week='',project_name='',project_id='',department_id='',department_name='',employee_name='',user_id=''):
    '''
    给sql加入筛选条件
    '''
    select_param="*,dev.id as dev_event_id" 
    
    start_date, end_date=default_date(filter_date)
    print()
    if natural_week:
        start_date, end_date=get_first_day(natural_week)
    where_condition = u"dev.event_date>='{0}' and dev.event_date<='{1}' ".format(start_date, end_date)
    if project_name:
        where_condition += "and project.project_name like '%{0}%' ".format(project_name)
    if project_id:
        where_condition += "and project.id = '{0}' ".format(project_id)
    #筛选部门中所有人员
    if department_name:
        department_id=departmentname_to_departmentid(department_name)
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
    if employee_name:
        user_id=chinesename_to_userid(employee_name)                 
        where_condition += "and dev_event_owner_id = '{0}' ".format(user_id)

    plain_sql = u"SELECT {0} FROM api_devevent as dev left join api_devproject as project on dev.dev_event_project_id = project.id \
        left join api_deveventtype on dev.dev_event_type_id = api_deveventtype.id \
        left join accounts_user  on accounts_user.id = dev.dev_event_owner_id \
        where {1} order by dev.event_date,dev.start_time".format(
        select_param, where_condition)        
    return plain_sql

def filter_sale_event_sql(filter_date='',natural_week='',user_id='',customer_id='',department_name='',employee_name=''):
    '''
    给sql加入筛选条件
    '''
    sale_event_field = ["sale.id as sale_event_id", "cus_con_post", "visit_date", "cus_con_mdn", "cus_con_tel_num", "cus_con_wechart", "communicate_record", "sale_event_remark"]
    active_type_field=['active_type_name']
    sale_customer_field=['customer.id as customer_id','short_name ']
    sale_phase_field=['phase_name']
    user_field=['chinese_name','accounts_user.id as user_id']
    all_select_field = sale_event_field + active_type_field + sale_customer_field+sale_phase_field+user_field
    select_param = ",".join(all_select_field)

    start_date, end_date=default_date(filter_date)
    if natural_week:
        start_date, end_date=get_first_day(natural_week)
    where_condition = u"sale.visit_date>='{0}' and sale.visit_date<='{1}' ".format(start_date, end_date)

    #筛选部门中所有人员
    if department_name:
        department_id=departmentname_to_departmentid(department_name)
        user_queryset=User.objects.filter(department_id=department_id).all()
        user_ids=tuple([i.id for i in user_queryset])           
        if user_ids:
            #如果user_ids只有1个数，则python会因为元祖在后面加一个“，”，导致sql无法执行
            if len(user_ids)==1:
                where_condition += "and sale_event_owner_id =  {0} ".format(user_ids[0])
            else:
                where_condition += "and sale_event_owner_id in  {0} ".format(user_ids)

    #筛选记录所属人
    if  user_id:     
        where_condition += "and sale_event_owner_id = '{0}' ".format(user_id)

    if customer_id:
        where_condition += "and customer.id = '{0}' ".format(customer_id)


    if employee_name:
        owner_id=chinesename_to_userid(employee_name)
        where_condition += "and sale_event_owner_id = '{0}' ".format(owner_id)

    plain_sql = u"SELECT {0} FROM api_saleevent as sale\
        left join api_saleactivetype as type on sale.active_type_id = type.id \
        left join api_salecustomer as customer on sale.sale_customer_id = customer.id \
        left join api_salephase as phase on sale.sale_phase_id = phase.id \
        left join accounts_user  on accounts_user.id = sale.sale_event_owner_id \
        where {1} ".format(select_param,where_condition)

    return plain_sql


def pivot_target_actual_sql(natural_week='',filter_sql='',department_name=''):
    '''
    先查出部门内所有人的目标，再连接实际情况，再行转列显示出对比表
    '''
    if department_name:
        department_id=departmentname_to_departmentid(department_name)
        user_queryset=User.objects.filter(department_id=department_id).all()
        user_ids=tuple([i.id for i in user_queryset])           
        if user_ids:
            #如果user_ids只有1个数，则python会因为元祖在后面加一个“，”，导致sql无法执行
            if len(user_ids)==1:
                where_condition = "and sale_target_owner_id =  {0} ".format(user_ids[0])
            else:
                where_condition = "and sale_target_owner_id in  {0} ".format(user_ids)
    target_sql=u"select sale_target_owner_id,phase_name as target_phase_name,target from api_saletarget\
        where natural_week='{0}' {1}  ".format(natural_week,where_condition)

    #统计销售员一周拜访次数
    group_sql = u'select child.user_id,child.chinese_name,child.phase_name,count(child.phase_name) as phase_count \
        from ({0}) as child group by child.phase_name,child.chinese_name,child.user_id '.format(filter_sql)

    print group_sql
    union_sql=u'''select  a_user.chinese_name,phase_name,phase_count,target_phase_name,target \
                    from ({1}) as target left join ({0}) as group_count on \
                    target.sale_target_owner_id=group_count.user_id and target.target_phase_name=group_count.phase_name
                    left join accounts_user as a_user on  target.sale_target_owner_id=a_user.id'''.format(group_sql,target_sql)
    pivot_sql=u'''select chinese_name,   
 
            sum(case when phase_name = 'B' then phase_count else 0 end) as "B",  
            sum(case when phase_name = 'C' then phase_count else 0 end) as "C",
            sum(case when phase_name = 'D' then phase_count else 0 end) as "D",
            sum(case when phase_name = 'E' then phase_count else 0 end) as "E",
            sum(case when phase_name = 'F' then phase_count else 0 end) as "F",
            sum(case when phase_name = 'G' then phase_count else 0 end) as "G", 
            sum(case when target_phase_name = 'B' then target else 0 end) as "target_B",  
            sum(case when target_phase_name = 'C' then target else 0 end) as "target_C",
            sum(case when target_phase_name = 'D' then target else 0 end) as "target_D",
            sum(case when target_phase_name = 'E' then target else 0 end) as "target_E",
            sum(case when target_phase_name = 'F' then target else 0 end) as "target_F",
            sum(case when target_phase_name = 'G' then target else 0 end) as "target_G"       
            from  ({0}) as group_sql group by chinese_name order by chinese_name desc;  '''.format(union_sql)
    return pivot_sql

def chinesename_to_userid(employee_name=''):
    user_queryset=User.objects.filter(chinese_name=employee_name)
    if user_queryset:
        user_id=user_queryset.first().id
    else:
        user_id=-1     
    return user_id

def departmentname_to_departmentid(department_name=''):      
    department_queryset=Department.objects.filter(department_name=department_name)
    if department_queryset:
        department_id=department_queryset.first().id
    else:
        department_id=-1
    return department_id

def userid_to_chinesename(source_ids):
    '''
    根据user id来查找中文名
    '''
    id_list= source_ids.split(',')
    chinese_name_list=[]            
    for i in id_list:
        chinese_name_queryset=User.objects.filter(id=i)
        if chinese_name_queryset:
            chinese_name=chinese_name_queryset.first().chinese_name
            chinese_name_list.append(chinese_name)                
    result=u'，'.join(chinese_name_list)
    return result