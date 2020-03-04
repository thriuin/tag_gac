from rest_framework import serializers
from api.models import Entities, ValueThreshold, \
    CommodityType, CommodityCodeSystem, Code,\
    TenderingReason, TAException, CftaException


class EntitiesSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.Entities'
    """
    class Meta:
        model = Entities
        fields = ['name', 'lang', 'ccfta', 'ccofta',
                  'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class ValueThresholdSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.ValueThreshold'
    """
    class Meta:
        model = ValueThreshold
        fields = ['type_value', 'lang', 'ccfta', 'ccofta',
                  'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class CommodityTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CommodityType
        fields=['commodity_type', 'lang']


class CommodityCodeSystemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.CommodityCodeSystem'
    """
    class Meta:
        model = CommodityCodeSystem
        fields = ['commodity_code_system', 'lang']


class CodeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.Code'
    """
    class Meta:
        model = Code
        fields = ['type', 'code_system',
                  'code', 'lang',
                  'ccfta', 'ccofta', 'chfta', 'cpafta',
                  'cpfta', 'ckfta', 'cufta', 'wto_agp',
                  'ceta', 'cptpp', 'cfta']


class TenderingReasonSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.TenderingReason'
    """
    class Meta:
        model = TenderingReason
        fields = ['name', 'lang', 'ccfta', 'ccofta',
                  'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class TAExceptionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.TAException'
    """
    class Meta:
        model = TAException
        fields = ['name', 'lang', 'ccfta', 'ccofta',
                  'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class CftaExceptionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.CftaException'
    """
    class Meta:
        model = CftaException
        fields = ['name', 'lang', 'ccfta', 'ccofta',
                  'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']