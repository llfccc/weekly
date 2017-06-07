from django.contrib import admin
from api.models import DevEvent,DevEventType,DevProject,WeekSummary,SaleActiveType,SaleCustomer,SalePhase,SaleTarget,SaleEvent
# Register your models here.

admin.site.register(DevEvent)
admin.site.register(DevEventType)
admin.site.register(DevProject)
admin.site.register(WeekSummary)
admin.site.register(SaleActiveType)
admin.site.register(SaleCustomer)
admin.site.register(SalePhase)
admin.site.register(SaleTarget)
admin.site.register(SaleEvent)