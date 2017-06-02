from django.contrib import admin
from api.models import DevProject,DevEventType
from api.models import SaleEvent
# Register your models here.
admin.site.register(DevProject)
admin.site.register(DevEventType)
admin.site.register(SaleEvent)