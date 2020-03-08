from guide.models import CommodityTypes, CommodityCodingSystem, CommodityCode, TenderingReason, TAException, ValueThreshold, CftaExceptions, Entities
from rest_framework import serializers


class CommodityTypesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CommodityTypes
        fields= ['type_en', 'type_fr']


class CommodityCodingSystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CommodityCodingSystem
        fields = ['system_en', 'system_fr']


class CommodityCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CommodityCode
        fields = ['commodity_type_en', 'commodity_type_fr', 'commodity_code_system_en', 'commodity_code_system_fr',
            'commodity_code_en', 'commodity_code_fr', 'nafta', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 
            'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp'
        ]

class TenderingReasonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TenderingReason
        fields = ['desc_en', 'desc_fr']


class EntitiesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entities
        fields = ['desc_en', 'desc_fr']


class TAExceptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TAException
        fields = ['nafta', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp' 'desc_en', 'desc_fr']


class ValueThresholdSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ValueThreshold
        fields = ['nafta', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp' 'type_value_en', 'type_value_fr']


class CftaExceptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CftaExceptions
        fields = ['nafta', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
            'wto_agp', 'ceta', 'cptpp' 'desc_en', 'desc_fr']
