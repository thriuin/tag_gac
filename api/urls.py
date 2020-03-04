from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from api.views import EntitiesView, ValueThresholdView, \
    CommodityTypeView, CommodityCodeSystemView, CodeView, \
    TAExceptionView, CftaExceptionView, TenderingReasonView

router = routers.SimpleRouter()
router.register(r'entities', EntitiesView)
router.register(r'value', ValueThresholdView)
router.register(r'commodity_type', CommodityTypeView)
router.register(r'commodity_system', CommodityCodeSystemView)
router.register(r'code', CodeView)
router.register(r'exceptions', TAExceptionView)
router.register(r'cfta_exceptions', CftaExceptionView)
router.register(r'limited_tendering', TenderingReasonView)

urlpatterns = router.urls