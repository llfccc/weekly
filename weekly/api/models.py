# coding=utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class JobContent(models.Model):
    operator= models.CharField(max_length=10,default='admin')
    work_title = models.CharField(max_length=1024)
    hided = models.BooleanField(default=0, verbose_name='是否隐藏')

    start_time = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    # cost_time = models.FloatField(null=True,blank=True,verbose_name='耗时')
    complete_status = models.IntegerField(default=0, verbose_name='完成状态')  # 0代表未完成，100代表已完成,其他数字代表百分比
    # follow_up = models.CharField(null=True, blank=True,max_length=1024)
    job_manager = models.CharField(null=True, blank=True, verbose_name='工作负责人', max_length=10)
    work_auditor = models.CharField(null=True, blank=True, verbose_name='工作审核人', max_length=10)
    remark = models.TextField(null=True, blank=True, verbose_name="备注")

    def __unicode__(self):
        return u"{}".format(self.work_title)
