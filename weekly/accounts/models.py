# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Department(models.Model):
    '''
    用户部门表
    '''
    department_name = models.CharField(max_length=100, verbose_name='活动类型名称')
    department_remark = models.CharField(max_length=64, null=True,
                              blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True)

    # owner_id =  models.IntegerField(verbose_name='创建人')
    def __unicode__(self):
        return u"{}".format(self.department_name)
    class Meta:
        permissions = (
            ("view_department", "可以查看部门"),
            # ("update_department", "可以修改部门"),
            # ("del_department", "可以删除部门"),
        )
    class Meta:  
        verbose_name_plural = '部门'  
class Position(models.Model):
    '''
    职位表
    '''
    position_name = models.CharField(max_length=100, verbose_name='职位名称')
    position_remark = models.CharField(max_length=64, null=True,blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True)

    # owner_id =  models.IntegerField(verbose_name='创建人')
    def __unicode__(self):
        return u"{}".format(self.position_name)
    # class Meta:
    #     permissions = (
    #         ("view_department", "可以查看部门"),
    #         # ("update_department", "可以修改部门"),
    #         # ("del_department", "可以删除部门"),
    #     )
    class Meta:  
        verbose_name_plural = '职位'  

class User(AbstractUser):     #继承AbstractUser
    describition = models.TextField(null=True,blank=True,verbose_name='描述说明（非必须）')
    chinese_name = models.CharField(max_length=64, null=True,blank=True,verbose_name='中文名')
    # department_id = models.IntegerField(null=True,blank=True,verbose_name='部门id')
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL,verbose_name='部门')
    position = models.ForeignKey(Position, blank=True, null=True, on_delete=models.SET_NULL,verbose_name='职位')

    def __unicode__(self):
        return u"{}".format(self.chinese_name)
    class Meta:
        permissions = (
            ("get_chinesename", "自定义：查看中文用户"),
            # ("update_department", "可以修改部门"),
            # ("del_department", "可以删除部门"),
        )
    class Meta:  
        verbose_name_plural = '用户'  



