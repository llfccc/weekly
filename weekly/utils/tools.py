# coding=utf-8
# 返回出口函数
import json
import logging
from django.http import HttpResponse
from django.forms.models import model_to_dict
import sys
import string, random
from hashlib import md5

reload(sys)
sys.setdefaultencoding("utf-8")
Logger = logging.getLogger("normal")

import json
import datetime


# 重写构造json类，遇到日期特殊处理
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
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


# 随机码生成
def get_random():
    base = string.ascii_letters + "0123456789" + "!@#$%^&*<>?~{}"
    src = "".join(random.sample(base, 16))
    m5 = md5()
    m5.update(src)
    return m5.hexdigest()

#获取当前日期的星期一及星期填的datetime
def getMondaySunday():
    today = datetime.date.today()
    Sunday = today + datetime.timedelta(6 - today.weekday())
    Monday  = today + datetime.timedelta(-today.weekday())
    return (Monday,Sunday)