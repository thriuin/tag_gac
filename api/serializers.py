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
        fields = ['name_en', 'name_fr', 'ccfta', 'ccofta',
                  'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class ValueThresholdSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.ValueThreshold'
    """
    class Meta:
        model = ValueThreshold
        fields = ['name_en', 'name_fr', 'ccfta', 'ccofta',
                  'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class CommodityTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CommodityType
        fields=['commodity_type_en', 'commodity_type_fr']


class CommodityCodeSystemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.CommodityCodeSystem'
    """
    class Meta:
        model = CommodityCodeSystem
        fields = ['commodity_code_system_en', 'commodity_code_system_fr']


class CodeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.Code'
    """
    class Meta:
        model = Code
        fields = ['type_en', 'type_fr',
                  'code_system_en', 'code_system_fr',
                  'code_en', 'code_fr',
                  'ccfta', 'ccofta', 'chfta', 'cpafta',
                  'cpfta', 'ckfta', 'cufta', 'wto_agp',
                  'ceta', 'cptpp', 'cfta']


class TenderingReasonSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.TenderingReason'
    """
    class Meta:
        model = TenderingReason
        fields = ['name_en', 'name_fr', 'ccfta', 'ccofta',
                  'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class TAExceptionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.TAException'
    """
    class Meta:
        model = TAException
        fields = ['name_en', 'name_fr', 'ccfta', 'ccofta',
                  'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class CftaExceptionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.CftaException'
    """
    class Meta:
        model = CftaException
        fields = ['name_en', 'name_fr', 'ccfta', 'ccofta',
                  'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']