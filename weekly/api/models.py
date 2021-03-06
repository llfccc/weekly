# coding=utf-8
from __future__ import unicode_literals
from django.db import models
# from django.contrib.auth.models import User
from accounts.models import User

# Create your models here.


class DevProject(models.Model):
    available_choice=((0,"启用"),(1,"禁用"))
    project_name = models.CharField(max_length=100, verbose_name='项目名称')
    closed_status=models.IntegerField(choices=available_choice,default=0,verbose_name="1代表关闭")   #当前项目是否启用
    create_time = models.DateTimeField(auto_now_add=True)
    project_creator= models.ForeignKey(User,blank=True, null=True, on_delete=models.SET_NULL,verbose_name='创建人')
    dev_project_remark = models.CharField(max_length=64, null=True,
                                          blank=True, verbose_name='备注')
    def __unicode__(self):
        return u"{}".format(self.project_name)         
        
    class Meta:
        permissions = (
        ("view_devproject", u"技术员工：查看项目名称"),
        )
        # verbose_name_plural = '信息统计' 
        verbose_name_plural = '项目' 
class DevEventType(models.Model):
    available_choice=((0,"启用"),(1,"禁用"))
    event_type_name = models.CharField(max_length=100, verbose_name='事件类型名称')
    dev_event_type_remark = models.CharField(max_length=64, null=True,
                                             blank=True, verbose_name='备注')
    closed_status=models.IntegerField(choices=available_choice,default=0,verbose_name="1代表关闭")   #当前项目是否启用
    create_time = models.DateTimeField(auto_now_add=True)

    # creator =  models.ForeignKey(User, verbose_name='创建人')
    def __unicode__(self):
        return u"{}".format(self.event_type_name)
        
    class Meta:
        permissions = (
        ("view_deveventtype", u"技术员工：查看事件类型"),
        )
        verbose_name_plural = '事件类型' 


class DevEvent(models.Model):
    description = models.CharField(
        null=True, blank=True, max_length=500, verbose_name='事件描述')
    event_date=models.DateField(verbose_name='事件日期')
    start_time = models.TimeField(verbose_name='事件开始时间')
    end_time = models.TimeField(verbose_name='事件结束时间')
    duration_time= models.FloatField(verbose_name='工作时长(秒)')
    fin_percentage = models.IntegerField(default=0, verbose_name='完成百分比')
    up_reporter_id = models.CharField(max_length=64, verbose_name='上游汇报人')
    down_reporter_ids = models.CharField(max_length=64, verbose_name='下游交接人')
    dev_event_remark = models.TextField(
        null=True, blank=True, verbose_name="备注")
    dev_event_create_time = models.DateTimeField(auto_now_add=True)

    dev_event_owner = models.ForeignKey(User, verbose_name='事件所属人')
    dev_event_project_id = models.IntegerField(blank=True,null=True, verbose_name='所属项目')
    dev_event_type = models.ForeignKey(DevEventType, verbose_name='事件类型')

    def __unicode__(self):
        return u"{}".format(self.description)

    # def time_cousuming(self, keyword):
    #     return self.start_time-self.end_time
    class Meta:
        permissions = (
        ("view_devevent", u"技术员工：查看本人的事件"),
        ("insert_devevent", "技术员工：新增工作事件"),
        ("export_excel", u"技术员工：导出本人的事件为excel"),
        ("analysis_devevent", "技术主管：分析周报事件"),    
        ("markDel_devevent", u"技术员工:标记删除自己的工作事件"),
  

        )
        verbose_name_plural = '周报事件' 

        

class WeekSummary(models.Model):
    natural_week = models.CharField(max_length=64, verbose_name='自然周')
    summary = models.CharField(max_length=500, verbose_name='总结')
    self_evaluation = models.CharField(max_length=500, verbose_name='自我评价')
    plan = models.CharField(max_length=500, verbose_name='计划')
    create_time = models.DateTimeField(auto_now_add=True)
    summary_owner = models.ForeignKey(User, verbose_name='事件所属人')

    def __unicode__(self):
        return u"{}".format(self.summary)

    class Meta:
        permissions = (
        ("view_weeksummary", u"所有员工:查看员工自己的周报总结"),
        ("insert_weeksummary", u"所有员工:新增自己的周报总结"),
        ("markDel_weeksummary", u"所有员工:标记删除自己的周报总结"),
        ("analysis_weekly_summary", u"所有主管:查看员工每周周报总结"),
        
        # ("close_task", "Can remove a task by setting its status as closed"),
        )
        verbose_name_plural = '周报总结'    


class SaleActiveType(models.Model):
    available_choice=((0,"启用"),(1,"禁用"))

    active_type_name = models.CharField(max_length=100, verbose_name='活动类型名称')
    sale_active_type_remark = models.CharField(max_length=64, null=True,
                                               blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True)
    closed_status=models.IntegerField(choices=available_choice,default=0,verbose_name="1代表关闭")   #当前项目是否启用

    def __unicode__(self):
        return u"{}".format(self.active_type_name)
    class Meta:  
        permissions = (
            ("view_SaleActivateType", u"销售员工:查看销售活动类型"),
        )
        verbose_name_plural = '活动类型'  

class SaleCustomer(models.Model):
    '''
    客户信息表
    '''
    full_name = models.CharField(null=False,blank=False,max_length=100, verbose_name='客户全称')
    short_name = models.CharField(null=False,blank=False,max_length=100, verbose_name='客户简称')
    contact_post = models.CharField(null=False,blank=False,max_length=100, verbose_name='主要联系人职位')
    contact_name = models.CharField(null=False,blank=False,max_length=100, verbose_name='主要联系人姓名')
    contact_mdn = models.CharField(null=False,blank=False,max_length=100, verbose_name='主要联系人手机号码')
    contact_tel_num = models.CharField(
        max_length=100, verbose_name='主要联系人电话号码')
    sale_customer_remark = models.CharField(max_length=64, null=True,
                                            blank=True, verbose_name='客户备注')
    sale_customer_owner = models.ForeignKey(User, verbose_name='客户添加人')

    create_time = models.DateTimeField(auto_now_add=True)
    available_choice=((0,"启用"),(1,"禁用"))
    closed_status=models.IntegerField(choices=available_choice,default=0,verbose_name="1代表关闭")   #当前项目是否启用


    def __unicode__(self):
        return u"{}".format(self.full_name)
    class Meta:  
        permissions = (
            ("view_SaleCustomer", u"销售员工:查看销售客户"),
            ("insert_salecustomer", u"销售员工:增加销售客户"),
        )
        verbose_name_plural = '客户信息'  

class SalePhase(models.Model):
    phase_name = models.CharField(
        max_length=64, verbose_name='阶段名称，例如B,C,D,E,F,G')
    description = models.CharField(
        null=True, blank=True, max_length=500, verbose_name='阶段描述')
    phase_count = models.IntegerField(verbose_name='最大拜访次数')
    sale_phase_remark = models.CharField(max_length=64, null=True,
                                         blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True)
    available_choice=((0,"启用"),(1,"禁用"))
    closed_status=models.IntegerField(choices=available_choice,default=0,verbose_name="1代表关闭")   #当前项目是否启用

    # creator =models.ForeignKey(User, verbose_name='创建人')

    def __unicode__(self):
        return u"{}".format(self.phase_name)
    class Meta:  
        permissions = (
            ("view_SalePhase", u"销售员工:查看销售阶段"),
        )
        verbose_name_plural = '销售阶段'


class SaleTarget(models.Model):
    natural_week = models.CharField(max_length=64, verbose_name='自然周,如 2017-10 ')
    phase_name = models.ForeignKey(SalePhase,verbose_name='阶段名称')
    target = models.IntegerField(verbose_name='目标')
    phase_count = models.IntegerField(verbose_name='最大拜访次数')
    sale_target_remark = models.CharField(max_length=64, null=True,
                                          blank=True, verbose_name='销售目标备注')
    create_time = models.DateTimeField(auto_now_add=True)
    # creator =  models.ForeignKey(User, verbose_name='创建人')
    sale_target_owner = models.ForeignKey(User,verbose_name='目标所属人')

    def __unicode__(self):
        return u"{0}--{1}--{2}".format(self.natural_week,self.phase_name,self.sale_target_owner)

    class Meta:  
        verbose_name_plural = '销售目标'  
        unique_together = ('natural_week', 'phase_name','sale_target_owner')

class SaleEvent(models.Model):
    cus_con_post = models.CharField(max_length=500, verbose_name='客户职位')
    visit_date = models.DateField(verbose_name='拜访时间')
    # end_time = models.DateTimeField(verbose_name='结束时间')
    cus_con_mdn = models.CharField(
        max_length=64, default=None, verbose_name='手机号码')
    cus_con_tel_num = models.CharField(max_length=64, verbose_name='客户电话号码')
    cus_con_wechart = models.CharField(max_length=64, verbose_name='客户的微信号')
    communicate_record = models.CharField(max_length=500, verbose_name='沟通成果')
    sale_event_remark = models.TextField(
        null=True, blank=True, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True)

    sale_event_owner = models.ForeignKey(User, verbose_name='拜访人')
    active_type = models.ForeignKey(SaleActiveType, verbose_name='拜访类型')
    sale_customer = models.ForeignKey(SaleCustomer, verbose_name='客户ID')
    sale_phase = models.ForeignKey(SalePhase, verbose_name='拜访阶段')

    def __unicode__(self):
        return u"{}".format(self.visit_date)
        
    class Meta:
        permissions = (            
            ("view_SaleEvent", u"销售员工:查看销售拜访事件"),
            ("insert_saleevent", u"销售员工:新增销售拜访事件"),
            ("markDel__saleevent", u"销售员工:标记删除销售拜访事件"),
            ("analysis_sale_event", u"销售主管:分析销售拜访事件"),
            ("display_sale_event", u"销售主管:查询销售拜访事件"),    
        )
        verbose_name_plural = '销售事件'
