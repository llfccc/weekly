# coding=utf-8
# 返回出口函数
import json
import logging
from django.http import HttpResponse
from django.forms.models import model_to_dict
import sys
reload(sys)
sys.setdefaultencoding( "utf-8")
Logger = logging.getLogger("normal")

def my_response(code, msg, content="", status_code=200, content_type="text/json"):
    if code != 0:
        Logger.info("request handler error, return data is:: {}".format(msg))
    data = json.dumps({"code": code, "msg": msg, "content": content})
    response = HttpResponse(data, status=status_code, content_type=content_type)
    response["Access-Control-Allow-Origin"] = "*,http://localhost:8080,http://127.0.0.1:8080,http://localhost,http://127.0.0.1"  # 如果要所有访问则属性设置为*，但不合适
    response["Access-Control-Allow-Headers"] = "Access-Control-Allow-Origin, x-requested-with, content-type"
    return response


def queryset_to_json(queryset, query_field):
    job_output_list = []
    for query in queryset:
        query = model_to_dict(query)
        job_dict = {}
        for field in query_field:
            job_dict[field] = query.get(field, '')
        job_output_list.append(job_dict)
    data = json.dumps(job_output_list)
    return data
