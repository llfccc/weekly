from django.contrib import admin
from api.models import DevEvent,DevEventType,DevProject,WeekSummary,SaleActiveType,SaleCustomer,SalePhase,SaleTarget,SaleEvent
import xadmin
# Register your models here.
#class FelixProjectsAdmin(admin.ModelAdmin):
# class ApiProjectsAdmin(object):
#     list_display = ('pj_name', 'pj_group', 'pj_category')

# xadmin.site.register(FelixProjects, FelixProjectsAdmin)\
xadmin.site.register(DevEvent)
xadmin.site.register(DevEventType)
xadmin.site.register(DevProject)
xadmin.site.register(WeekSummary)
xadmin.site.register(SaleActiveType)
xadmin.site.register(SaleCustomer)
xadmin.site.register(SalePhase)
xadmin.site.register(SaleTarget)
xadmin.site.register(SaleEvent)
