# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import xadmin
from django.contrib import admin
from accounts.models import  Department
from api.models import SaleTarget,SalePhase,DevProject
from accounts.models import Position

# Register your models here.
class SaleTargetAdmin(object):
    search_fields = ('natural_week', 'phase_name','target','phase_count')
    list_display =  ('natural_week', 'phase_name','target','phase_count','sale_target_owner')
    list_filter = ('natural_week','sale_target_owner')
    ordering = ('id','natural_week','phase_name',)

xadmin.site.register(Department)
xadmin.site.register(SaleTarget,SaleTargetAdmin)
xadmin.site.register(SalePhase)
xadmin.site.register(Position)
xadmin.site.register(DevProject)