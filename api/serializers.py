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
        fields = ['name_en', 'name_fr', 'ccfta', 'ccofta',
                  'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class CodeListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for :model: 'guide.CodeList'
    """
    class Meta:
        model = CodeList
        fields = ['name_en', 'name_fr', 'code_en', 'code_fr',
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
