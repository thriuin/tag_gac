from api.models import Entities, ValueThreshold, \
    CommodityType, CommodityCodeSystem, Code, \
    TenderingReason, TAException, CftaException
from rest_framework import viewsets
from api.serializers import EntitiesSerializer, ValueThresholdSerializer, \
    CommodityTypeSerializer, CommodityCodeSystemSerializer, CodeSerializer, \
    TenderingReasonSerializer, TAExceptionSerializer, CftaExceptionSerializer


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


class CommodityTypeView(viewsets.ModelViewSet):
    '''
    API endpoint for :model: 'api.CommodityType'
    '''
    queryset = CommodityType.objects.all().order_by('commodity_type_en')
    serializer_class = CommodityTypeSerializer

class CommodityCodeSystemView(viewsets.ModelViewSet):
    """
    API endpoint for :model: 'api.CommodityCodeSystem'
    """
    queryset = CommodityCodeSystem.objects.all().order_by('commodity_code_system_en')
    serializer_class = CommodityCodeSystemSerializer


class CodeView(viewsets.ModelViewSet):
    """
    API endpoint for :model: 'api.Code'
    """
    queryset = Code.objects.all().order_by('code_system_en')
    serializer_class = CodeSerializer


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
