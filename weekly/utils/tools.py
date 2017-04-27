# coding=utf-8
# 返回出口函数
import json
import logging
from django.http import HttpResponse
from django.forms.models import model_to_dict
import sys
import xlsxwriter

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
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
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
    job_output_list = []
    for query in queryset:
        query = model_to_dict(query)
        job_dict = {}
        for field in query_field:
            job_dict[field] = query.get(field, '')
        job_output_list.append(job_dict)
    return job_output_list


def dict_to_json(data_list):
    data = json.dumps(data_list, cls=CJsonEncoder)
    return data


class ReportExcel(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('hello.xlsx')  # 建立文件
        self.worksheet = self.workbook.add_worksheet()  # 建立sheet， 可以work.add_worksheet('employee')来指定sheet名，但中文名会报UnicodeDecodeErro的错误
        self.merge_format_title = self.workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#D7E4BC',
        })
        self.merge_format_title2 = self.workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
        })
        self.merge_format = self.workbook.add_format({
            'align': 'left',
            'valign': 'vcenter',
        })

    def write_excel(self, data):
        worksheet = self.worksheet
        worksheet.merge_range('A1:M1', u'周工作总结表', self.merge_format_title)
        worksheet.merge_range('A2:M2', u'{}--{}'.format('A', 'B'), self.merge_format_title2)
        worksheet.merge_range('A3:M3', u'本周工作重点：{}'.format('A'), self.merge_format)
        worksheet.merge_range('A4:M4', u'上周未完成工作：{}'.format('B'), self.merge_format)
        title = (
            [u'日期', u'星期', u'事件', u'所属项目', u'工作内容', u'所花时间（按分钟计算）', u'累计工作时间', u'真实工作时间', u'完成情况（%）', u'后续跟踪', u'工作负责人',
             u'工作审核人', u'备注'
             ])
        row = 4
        col = 0
        for t in title:
            worksheet.write(row, col, t)
            col += 1
        data_list = []
        if not data:
            data_list = (
                [u'帮助新人装系统', 60, 7.5, 60, 100, '', u'田毅', u'', u'备注'],
                [u'学些vue', 120, 7.5, 60, 100, '', u'田毅', u'', u'备注2'],)
        else:
            queue_list = ["work_title", "", "", "", "complete_status", ""]
            for item in data:
                temp_list = []
                for key in queue_list:
                    temp_list.append(item.get(key))
                data_list.append(temp_list)
        print(data)
        row = 5
        for r in data_list:
            col = 4
            for c in r:
                worksheet.write(row, col, c)
                col += 1
            row += 1
        self.workbook.close()
        return
