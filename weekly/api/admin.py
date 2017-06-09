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

class DevEventTypeAdmin(admin.ModelAdmin):
    search_fields = ('event_type_name', 'closed_status')
    list_display =  ('event_type_name', 'closed_status','dev_event_type_remark')
    list_filter = ('event_type_name','closed_status')
    ordering = ('id','event_type_name')


class SalePhaseAdmin(admin.ModelAdmin):
    search_fields = ('phase_name', 'description')
    list_display =  ('phase_name', 'phase_count','available_choice', 'description','dev_event_type_remark')
    list_filter = ('phase_name','available_choice')
    ordering = ('id','phase_name')


admin.site.register(DevEvent)
admin.site.register(DevEventType,DevEventTypeAdmin)
admin.site.register(DevProject)
# admin.site.register(WeekSummary)
admin.site.register(SaleActiveType,SaleActiveTypeAdmin)
# admin.site.register(SaleCustomer)
admin.site.register(SalePhase)
admin.site.register(SaleTarget,SaleTargetAdmin)
