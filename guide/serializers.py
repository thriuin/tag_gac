from guide.models import GoodsCode, ConstructionCode, ServicesCode, TenderingReason, FederalEntities
from rest_framework import serializers


class GoodsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodsCode
        fields = ['fs_code', 'fs_code_desc', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class ConstructionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConstructionCode
        fields = ['fs_code', 'fs_code_desc', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class ServicesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServicesCode
        fields = ['nafta_code', 'ccs_level_2', 'gsin_class', 'desc_en', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta',
                  'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']


class TenderingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TenderingReason
        fields = ['desc_en', 'desc_fr']


class FederalEntitiesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FederalEntities
        fields = ['name_en, name_fr']