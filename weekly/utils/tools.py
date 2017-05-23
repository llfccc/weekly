# coding=utf-8
# 返回出口函数
import json
import logging
import sys
import string, random
import datetime
from hashlib import md5
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.core.cache import cache
import decimal

reload(sys)
sys.setdefaultencoding("utf-8")
Logger = logging.getLogger("normal")


from django.db import connection, transaction

# 重写构造json类，遇到日期特殊处理
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
        elif isinstance(obj,decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def my_response(code, msg, content="", status_code=200, content_type="text/json"):
    if code != 0:
        Logger.info("request handler error, return data is:: {}".format(msg))
    data = json.dumps({"code": code, "msg": msg, "content": content})
    response = HttpResponse(data, status=status_code, content_type=content_type)
    response[
        "Access-Control-Allow-Origin"] = "*,http://localhost:8080,http://127.0.0.1:8080,http://localhost,http://127.0.0.1"  # 如果要所有访问则属性设置为*，但不合适
    response["Access-Control-Allow-Headers"] = "Access-Control-Allow-Origin, x-requested-with, content-type"
    return response


def queryset_to_dict(queryset, query_field):
    '''
    只返回query_field中存在的字段，防止数据泄露
    '''
    output_list = []
    for query in queryset:
        query = model_to_dict(query)
        job_dict = {}
        for field in query_field:
            job_dict[field] = query.get(field, '')
        output_list.append(job_dict)
    return output_list


def dict_to_json(data_list):
    data = json.dumps(data_list, cls=CJsonEncoder)
    return data



def get_random():
    '''
    随机码生成
    '''
    base = string.ascii_letters + "0123456789" + "!@#$%^&*<>?~{}"
    src = "".join(random.sample(base, 16))
    m5 = md5()
    m5.update(src)
    return m5.hexdigest()


def getMondaySunday():
    '''
    获取当前日期的星期一及星期填的datetime
    '''
    today = datetime.date.today()
    Sunday = today + datetime.timedelta(6 - today.weekday())
    Monday  = today + datetime.timedelta(-today.weekday())
    return (Monday,Sunday)



def fetch_data(sql):
    '''
    通过sql 获取数据,返回元祖
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        col_names = [desc[0] for desc in cursor.description]

        sql_result = cursor.fetchall()
        results = []

        for row in sql_result:
            if row is None:
                break
            results.append(dict(zip(col_names, row)))
    return results



def get_user_id(request):
    '''
    从缓存中获取当前用户的userid
    '''
    sid=request.COOKIES.get("sid",'')
    user_object=cache.get(sid)
    try:
        user_id=user_object.get("user_id")
    except:
        user_id=0
    return user_id


def getfirstday(weekflag):     
    '''
    根据周数获得每周的起始和结束日期,传入的值例如“2017-01-5周”
    '''

    yearnum = weekflag[0:4]   #取到年份
    weeknum = weekflag[5:7]   #取到周
    stryearstart = yearnum +'0101'   #当年第一天

    yearstart = datetime.datetime.strptime(stryearstart,'%Y%m%d') #格式化为日期格式
    yearstartcalendarmsg = yearstart.isocalendar()  #当年第一天的周信息
    yearstartweek = yearstartcalendarmsg[1]  
    yearstartweekday = yearstartcalendarmsg[2]
    yearstartyear = yearstartcalendarmsg[0]
    if yearstartyear < int (yearnum):
        daydelat = (8-int(yearstartweekday))+(int(weeknum)-1)*7
    else :
        daydelat = (8-int(yearstartweekday))+(int(weeknum)-2)*7     
    first_day = (yearstart+datetime.timedelta(days=daydelat)).date()
    last_day =first_day+datetime.timedelta(days=6)
    start_date=first_day.strftime("%Y-%m-%d")
    end_date=last_day.strftime("%Y-%m-%d")
    return (start_date,end_date)

def day_of_week(source):
    '''
    计算某一天是星期几，输入格式为 2017-1-1
    '''
    week_list=['星期日','星期一','星期二','星期三','星期四','星期五','星期六']

    if isinstance(source, datetime.datetime):
        date=source           
    elif isinstance(source, datetime.date):
        date=source
    else:
        return -1
    week_id=int(date.strftime("%w"))
    which_day=week_list[week_id]
    return   which_day

# def day_of_week(source):
#     '''
#     计算某一天是星期几，输入格式为 2017-1-1
#     '''
#     if isinstance(source, datetime.datetime):
#         date=datetime.datetime.strptime(source,'%Y-%m-%d %H:%M:%S')
#     elif isinstance(source, datetime.date):
#         date=datetime.datetime.strptime(source,"%Y-%m-%d")
#     else:
#         return -1
#     week_id=int(date.strftime("%w"))
#     which_day=week_list[week_id]
#     return which_day