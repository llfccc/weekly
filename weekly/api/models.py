# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User 


# Create your models here.
class DevProject(models.Model):
    project_name= models.CharField(max_length=100,verbose_name='项目名称')    
    creator_id=models.IntegerField(verbose_name='创建人')
    status= models.CharField(max_length=64,verbose_name='项目状态：00，关闭；01，启动')
    remark= models.CharField(max_length=64,null=True,blank=True,verbose_name='备注')
    create_time= models.DateTimeField(auto_now_add=True) 

    def __unicode__(self):
        return u"{}".format(self.project_name)

        
class DevEventType(models.Model):
    event_type_name= models.CharField(max_length=100,verbose_name='事件类型名称')   
    remark= models.CharField(max_length=64,null=True,blank=True,verbose_name='备注')
    creator_id=models.IntegerField(verbose_name='创建人')
    create_time= models.DateTimeField(auto_now_add=True) 

    def __unicode__(self):
        return u"{}".format(self.event_name)

class DevEvent(models.Model):
    description =models.CharField(max_length=500,verbose_name='事件描述')
    start_time = models.DateTimeField( verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    fin_percentage = models.IntegerField(default=0, verbose_name='完成百分比') 
    up_reporter_id=models.CharField(max_length=64,verbose_name='上游汇报人')
    down_reporter_ids=models.CharField(max_length=64,verbose_name='下游汇报人')
    remark = models.TextField(null=True, blank=True, verbose_name="备注")
    create_time= models.DateTimeField(auto_now_add=True)

    owner= models.ForeignKey(User, verbose_name='事件所属人')    
    project= models.ForeignKey(DevProject, verbose_name='所属项目')    
    event_type = models.ForeignKey(DevEventType, verbose_name='事件类型')



    def __unicode__(self):
        return u"{}".format(self.description)



class WeekSummary(models.Model):

    start_time = models.DateTimeField( verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    summary=models.CharField(max_length=500,verbose_name='总结')
    self_evaluation=models.CharField(max_length=500,verbose_name='总结')
    plan=models.CharField(max_length=500,verbose_name='总结')
    create_time= models.DateTimeField(auto_now_add=True)

    owner= models.ForeignKey(User, verbose_name='事件所属人')    
