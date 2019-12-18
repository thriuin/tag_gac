from guide.models import GoodsCodes, ConstructionCodes, ServicesCodes, TenderingReasons
from rest_framework import serializers


class GoodsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodsCodes
        fields = ['fs_code', 'fs_code_desc', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp']

class ConstructionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConstructionCodes
        fields = ['fs_code', 'fs_code_desc', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp']

class ServicesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServicesCodes
        fields = ['nafta_code', 'ccs_level_2', 'gsin_class', 'desc_en', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta',
                  'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp']


class TenderingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TenderingReasons
        fields = ['desc_en', 'desc_fr']