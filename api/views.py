from api.models import Entities, ValueThreshold, CommodityCodeSystem, \
    CodeList, TenderingReason, TAException, CftaException
from rest_framework import viewsets
from api.serializers import EntitiesSerializer, ValueThresholdSerializer, \
    CommodityCodeSystemSerializer, CodeListSerializer, \
    TenderingReasonSerializer, TAExceptionSerializer, \
    CftaExceptionSerializer


class EntitiesView(viewsets.ModelViewSet):
    """
    API endpoint for :model: 'api.Entities'
    """
    queryset = Entities.objects.all().order_by('name_en')
    serializer_class = EntitiesSerializer


class ValueThresholdView(viewsets.ModelViewSet):
    """
    API endpoint for :model: 'api.ValueThreshold'
    """
    queryset = ValueThreshold.objects.all()
    serializer_class = ValueThresholdSerializer


class CommodityCodeSystemView(viewsets.ModelViewSet):
    """
    API endpoint for :model: 'api.CommodityCodeSystem'
    """
    queryset = CommodityCodeSystem.objects.all().order_by('commodity_code_system_en')
    serializer_class = CommodityCodeSystemSerializer


class CodeListView(viewsets.ModelViewSet):
    """
    API endpoint for :model: 'api.CodeList'
    """
    queryset = CodeList.objects.all().order_by('code_system_en')
    serializer_class = CodeListSerializer


class TenderingReasonView(viewsets.ModelViewSet):
    """
    API endpoint for :model: 'api.TenderingReason'
    """
    queryset = TenderingReason.objects.all().order_by('name_en')
    serializer_class = TenderingReasonSerializer


class TAExceptionView(viewsets.ModelViewSet):
    """
    API endpoint for :model: 'api.TAException'
    """
    queryset = TAException.objects.all().order_by('name_en')
    serializer_class = TAExceptionSerializer


class CftaExceptionView(viewsets.ModelViewSet):
    """
    API endpoint for :model: 'api.CftaException'
    """
    queryset = CftaException.objects.all().order_by('name_en')
    serializer_class = CftaExceptionSerializer
