# coding=utf-8
from __future__ import unicode_literals
from django.db import models
# from django.contrib.auth.models import User
from accounts.models import User

# Create your models here.


class DevProject(models.Model):
    project_name = models.CharField(max_length=100, verbose_name='项目名称')

    status = models.CharField(max_length=64, verbose_name='项目状态：00，关闭；01，启动')
    dev_project_remark = models.CharField(max_length=64, null=True,
                                          blank=True, verbose_name='备注')
    project_is_closed = models.BooleanField(default=False,verbose_name="true代表关闭")
    create_time = models.DateTimeField(auto_now_add=True)

    creator_id = models.IntegerField(null=True, verbose_name='创建人')

    def __unicode__(self):
        return u"{}".format(self.project_name)


class DevEventType(models.Model):
    event_type_name = models.CharField(max_length=100, verbose_name='事件类型名称')
    dev_event_type_remark = models.CharField(max_length=64, null=True,
                                             blank=True, verbose_name='备注')
    devEventType_is_closed = models.BooleanField(default=False,verbose_name="true代表关闭")
    create_time = models.DateTimeField(auto_now_add=True)

    # creator =  models.ForeignKey(User, verbose_name='创建人')
    def __unicode__(self):
        return u"{}".format(self.event_type_name)


class DevEvent(models.Model):
    description = models.CharField(
        null=True, blank=True, max_length=500, verbose_name='事件描述')
    event_date=models.DateField(verbose_name='事件日期')
    start_time = models.TimeField(verbose_name='事件开始时间')
    end_time = models.TimeField(verbose_name='事件结束时间')
    fin_percentage = models.IntegerField(default=0, verbose_name='完成百分比')
    up_reporter_id = models.CharField(max_length=64, verbose_name='上游汇报人')
    down_reporter_ids = models.CharField(max_length=64, verbose_name='下游交接人')
    dev_event_remark = models.TextField(
        null=True, blank=True, verbose_name="备注")
    dev_event_create_time = models.DateTimeField(auto_now_add=True)

    dev_event_owner_id = models.IntegerField(null=True, verbose_name='事件所属人')
    dev_event_project_id = models.IntegerField(null=True, verbose_name='所属项目')
    dev_event_type_id = models.IntegerField(null=True, verbose_name='事件类型')

    def __unicode__(self):
        return u"{}".format(self.description)

    def time_cousuming(self, keyword):
        return self.start_time-self.end_time


class WeekSummary(models.Model):
    start_date = models.DateField(verbose_name='起始日期')
    # end_date = models.DateField(verbose_name='结束日期')
    summary = models.CharField(max_length=500, verbose_name='总结')
    self_evaluation = models.CharField(max_length=500, verbose_name='自我评价')
    plan = models.CharField(max_length=500, verbose_name='计划')
    create_time = models.DateTimeField(auto_now_add=True)
    summary_owner_id = models.IntegerField(verbose_name='事件所属人')

    def __unicode__(self):
        return u"{}".format(self.summary)


class SaleActiveType(models.Model):
    active_type_name = models.CharField(max_length=100, verbose_name='活动类型名称')
    sale_active_type_remark = models.CharField(max_length=64, null=True,
                                               blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"{}".format(self.active_type_name)


class SaleCustomer(models.Model):
    '''
    客户信息表
    '''
    full_name = models.CharField(max_length=100, verbose_name='客户全称')
    short_name = models.CharField(max_length=100, verbose_name='客户简称')
    contact_post = models.CharField(max_length=100, verbose_name='主要联系人职位')
    contact_name = models.CharField(max_length=100, verbose_name='主要联系人姓名')
    contact_mdn = models.CharField(max_length=100, verbose_name='主要联系人手机号码')
    contact_tel_num = models.CharField(
        max_length=100, verbose_name='主要联系人电话号码')
    sale_customer_remark = models.CharField(max_length=64, null=True,
                                            blank=True, verbose_name='客户备注')
    sale_customer_owner_id = models.IntegerField( verbose_name='客户添加人')
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"{}".format(self.full_name)


class SalePhase(models.Model):
    phase_name = models.CharField(
        max_length=64, verbose_name='阶段名称，例如B,C,D,E,F,G')
    description = models.CharField(
        null=True, blank=True, max_length=500, verbose_name='阶段描述')
    phase_count = models.IntegerField(verbose_name='最大拜访次数')
    sale_phase_remark = models.CharField(max_length=64, null=True,
                                         blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True)

    # creator =models.ForeignKey(User, verbose_name='创建人')

    def __unicode__(self):
        return u"{}".format(self.phase_name)


class SaleTarget(models.Model):
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    target = models.CharField(max_length=500, verbose_name='目标，json存储')
    phase_count = models.IntegerField(verbose_name='最大拜访次数')
    sale_target_remark = models.CharField(max_length=64, null=True,
                                          blank=True, verbose_name='销售目标备注')
    create_time = models.DateTimeField(auto_now_add=True)

    # creator =  models.ForeignKey(User, verbose_name='创建人')
    sale_target_owner_id = models.IntegerField(verbose_name='目标所属人')

    def __unicode__(self):
        return u"{}".format(self.owner)


class SaleEvent(models.Model):
    cus_con_post = models.CharField(max_length=500, verbose_name='客户职位')
    visit_date = models.DateField(verbose_name='拜访时间')
    # end_time = models.DateTimeField(verbose_name='结束时间')
    cus_con_mdn = models.CharField(
        max_length=64, default=None, verbose_name='手机号码')
    cus_con_tel_num = models.CharField(max_length=64, verbose_name='客户联系方式')
    cus_con_wechart = models.CharField(max_length=64, verbose_name='客户的微信号')
    communicate_record = models.CharField(max_length=500, verbose_name='沟通成果')
    sale_event_remark = models.TextField(
        null=True, blank=True, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True)

    sale_event_owner_id = models.IntegerField(null=True, verbose_name='拜访人')
    active_type_id = models.IntegerField(null=True, verbose_name='拜访类型')
    sale_customer_id = models.IntegerField(null=True, verbose_name='客户ID')
    sale_phase_id = models.IntegerField(null=True, verbose_name='拜访阶段')

    def __unicode__(self):
        return u"{}".format(self.visit_date)
