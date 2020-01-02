from django.contrib import admin
from .models import GoodsCode, ConstructionCode, ServicesCode, TenderingReason, TAException, ValueThreshold

# Register your models here.
admin.site.register(GoodsCode)
admin.site.register(ConstructionCode)
admin.site.register(ServicesCode)
admin.site.register(TAException)
admin.site.register(TenderingReason)
admin.site.register(ValueThreshold)

