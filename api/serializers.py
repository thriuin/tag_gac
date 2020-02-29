from rest_framework import serializers
from api.models import Entities, ValueThreshold, CommodityCodeSystem, \
    CodeList, TenderingReason, TAException, CftaException


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


class CommodityCodeSystemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.CommodityCodeSystem'
    """
    class Meta:
        model = CommodityCodeSystem
        fields = ['commodity_type_en', 'commodity_type_fr', 'commodity_code_system_en', 'commodity_code_system_fr']


class CodeListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.CodeList'
    """
    class Meta:
        model = CodeList
        fields = ['code_system_en', 'code_system_fr',
                  'code_list_en', 'code_list_fr',
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