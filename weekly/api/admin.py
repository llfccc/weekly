from django.contrib import admin
from api.models import DevEvent,DevEventType,DevProject,WeekSummary,SaleActiveType,SaleCustomer,SalePhase,SaleTarget,SaleEvent
# Register your models here.


class SaleTargetAdmin(admin.ModelAdmin):
    search_fields = ('sale_target_owner','natural_week', 'phase_name','target','phase_count')
    list_display =  ('sale_target_owner','natural_week', 'phase_name','target','phase_count')
    list_filter = ('natural_week','sale_target_owner')
    ordering = ('id','natural_week','phase_name',)


class SaleActiveTypeAdmin(admin.ModelAdmin):
    search_fields = ('active_type_name', 'closed_status')
    list_display =  ('active_type_name', 'closed_status','sale_active_type_remark')
    list_filter = ('active_type_name','closed_status')
    ordering = ('id','active_type_name')


admin.site.register(DevEvent)
admin.site.register(DevEventType)
admin.site.register(DevProject)
# admin.site.register(WeekSummary)
admin.site.register(SaleActiveType,SaleActiveTypeAdmin)
# admin.site.register(SaleCustomer)
admin.site.register(SalePhase)
admin.site.register(SaleTarget,SaleTargetAdmin)
# admin.site.register(SaleEvent)