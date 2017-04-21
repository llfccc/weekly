# coding=utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class JobContent(models.Model):
    work_title = models.CharField(max_length=1024)
    hided = models.BooleanField(default=0, verbose_name='是否隐藏')

    # record_date = models.DateTimeField(verbose_name='开始时间')
    # start_date = models.DateTimeField()
    # end_date = models.DateTimeField()
    # cost_time = models.FloatField()
    # complete_status = models.FloatField()
    # follow_up = models.CharField(null=True, blank=True,max_length=1024)
    # job_manager = models.CharField()
    # work_auditor = models.CharField()


    def __unicode__(self):
        return u"{}".format(self.work_title)
