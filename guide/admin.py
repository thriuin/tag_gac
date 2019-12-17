from django.contrib import admin
from .models import GoodsCodes, ConstructionCodes, ServicesCodes, TenderingReasons

# Register your models here.
admin.site.register(GoodsCodes)
admin.site.register(ConstructionCodes)
admin.site.register(ServicesCodes)
admin.site.register(TenderingReasons)
