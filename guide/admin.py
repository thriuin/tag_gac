# from django.contrib import admin
# from .models import CommodityType, \
#     GoodsFscCode, GoodsUnspscCode, \
#     ServicesCcsCode, ServicesCpcCode, ServicesUnspscCode, \
#     ConstructionCcsCode, ConstructionCpcCode, ConstructionUnspscCode, \
#     CftaException, TenderingReason, TAException, ValueThreshold, FederalEntities
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
#
#
# # Django Import-Export Registration (see: https://django-import-export.readthedocs.io)
# '''
# Commodity Type
# '''
# class CommodityTypeResource(resources.ModelResource):
#
#     class Meta:
#         model = CommodityType
#
#
# '''
# Two Goods codes: FSC, UNSPSC
# '''
# class GoodsFscResource(resources.ModelResource):
#
#     class Meta:
#         model = GoodsFscCode
#
#
# class GoodsFscAdmin(ImportExportModelAdmin):
#     resource_class = GoodsFscResource
#
#
# class GoodsUnspscResource(resources.ModelResource):
#
#     class Meta:
#         model = GoodsUnspscCode
#
#
# class GoodsUnspscAdmin(ImportExportModelAdmin):
#     resource_clas = GoodsUnspscResource
#
#
# '''
# Three Construction Codes: CCS, CPC, UNSPSC
# '''
# class ConstructionCcsResource(resources.ModelResource):
#
#     class Meta:
#         model = ConstructionCcsCode
#
#
# class ConstructionCcsAdmin(ImportExportModelAdmin):
#     resource_class = ConstructionCcsResource
#
#
# class ConstructionCpcResource(resources.ModelResource):
#
#     class Meta:
#         model = ConstructionCpcCode
#
#
# class ConstructionCpcAdmin(ImportExportModelAdmin):
#     resource_class = ConstructionCpcResource
#
#
# class ConstructionUnspscResource(resources.ModelResource):
#
#     class Meta:
#         model = ConstructionUnspscCode
#
#
# class ConstructionUnspscAdmin(ImportExportModelAdmin):
#     resource_class = ConstructionUnspscResource
#
#
# '''
# Three services codes: CCS, CPC, UNSPSC
# '''
# class ServicesCcsResource(resources.ModelResource):
#
#     class Meta:
#         model = ServicesCcsCode
#
#
# class ServicesCcsAdmin(ImportExportModelAdmin):
#     resource_class = ServicesCcsResource
#
#
# class ServicesCpcResource(resources.ModelResource):
#
#     class Meta:
#         model = ServicesCpcCode
#
#
# class ServicesCpcAdmin(ImportExportModelAdmin):
#     resource_class = ServicesCpcResource
#
#
# class ServicesUnspscResource(resources.ModelResource):
#
#     class Meta:
#         model = ServicesUnspscCode
#
#
# class ServicesUnspscAdmin(ImportExportModelAdmin):
#     resource_class = ServicesUnspscResource
#
#
# '''
# Federal Entities
# '''
# class FederalEntitiesResource(resources.ModelResource):
#
#     class Meta:
#         model = FederalEntities
#
#
# class FederalEntitiesAdmin(ImportExportModelAdmin):
#     resource_class = FederalEntitiesResource
#
#
# # Register your models here.
# admin.site.register(CommodityType)
# admin.site.register(GoodsFscCode, GoodsFscAdmin)
# admin.site.register(GoodsUnspscCode, GoodsUnspscAdmin)
#
# admin.site.register(ConstructionCcsCode, ConstructionCcsAdmin)
# admin.site.register(ConstructionCpcCode, ConstructionCpcAdmin)
# admin.site.register(ConstructionUnspscCode, ConstructionUnspscAdmin)
#
# admin.site.register(ServicesCcsCode, ServicesCcsAdmin)
# admin.site.register(ServicesCpcCode, ServicesCpcAdmin)
# admin.site.register(ServicesUnspscCode, ServicesUnspscAdmin)
#
# admin.site.register(TAException)
# admin.site.register(CftaException)
# admin.site.register(TenderingReason)
# admin.site.register(ValueThreshold)
# admin.site.register(FederalEntities, FederalEntitiesAdmin)
#
#
