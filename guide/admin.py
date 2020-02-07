from django.contrib import admin
from .models import GoodsOGDCode, GoodsMilitaryCode, ConstructionCode, ServicesCode, TenderingReason, TAException, ValueThreshold, FederalEntities
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Django Import-Export Registration (see: https://django-import-export.readthedocs.io)
class GoodsOGDCodeResource(resources.ModelResource):

    class Meta:
        model = GoodsOGDCode


class GoodsOGDCodeAdmin(ImportExportModelAdmin):
    resource_class = GoodsOGDCodeResource


class GoodsMilitaryCodeResource(resources.ModelResource):

    class Meta:
        model = GoodsMilitaryCode


class GoodsMilitaryAdmin(ImportExportModelAdmin):
    resource_class = GoodsMilitaryCodeResource


class ConstructionCodeResource(resources.ModelResource):

    class Meta:
        model = ConstructionCode


class ConstructionCodeAdmin(ImportExportModelAdmin):
    resource_class = ConstructionCodeResource


class ServicesCodeResource(resources.ModelResource):

    class Meta:
        model = ServicesCode


class ServicesCodeAdmin(ImportExportModelAdmin):
    resource_class = ServicesCodeResource


class FederalEntitiesResource(resources.ModelResource):

    class Meta:
        model = FederalEntities


class FederalEntitiesAdmin(ImportExportModelAdmin):
    resource_class = FederalEntitiesResource


# Register your models here.
admin.site.register(GoodsOGDCode, GoodsOGDCodeAdmin)
admin.site.register(GoodsMilitaryCode, GoodsMilitaryAdmin)
admin.site.register(ConstructionCode, ConstructionCodeAdmin)
admin.site.register(ServicesCode, ServicesCodeAdmin)
admin.site.register(TAException)
admin.site.register(TenderingReason)
admin.site.register(ValueThreshold)
admin.site.register(FederalEntities, FederalEntitiesAdmin)


