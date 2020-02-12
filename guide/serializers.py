from guide.models import CommodityType, \
    GoodsFscCode, GoodsUnspscCode, \
    ServicesCcsCode, ServicesCpcCode, ServicesUnspscCode, \
    ConstructionCcsCode, ConstructionCpcCode, ConstructionUnspscCode, \
    CftaException, TenderingReason, TAException, FederalEntities

from rest_framework import serializers


'''
Commodity Type
'''
class CommodityTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CommodityType
        fields = ['commodity_type']


'''
Two Goods Codes: FSC, UNSPSC
'''
class GoodsFscSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodsFscCode
        fields = ['fsc_code', 'fsc_code_desc', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class GoodsUnspscSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodsUnspscCode
        fields = ['unspsc_code', 'unspsc_code_desc', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']

'''
Three Construction Codes: CCS, CPC, UNSPSC
'''
class ConstructionCcsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConstructionCcsCode
        fields = ['ccs_code', 'ccs_code_desc', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class ConstructionCpcSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConstructionCpcCode
        fields = ['cpc_code', 'cpc_code_desc', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class ConstructionUnspscSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConstructionUnspscCode
        fields = ['unspsc_code', 'unspsc_code_desc', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


'''
Three Services Codes: CCS, CPC, UNSPSC
'''
class ServicesCcsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServicesCcsCode
        fields = ['ccs_code', 'ccs_code_desc', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta',
                  'wto_agp', 'ceta', 'cptpp', 'cfta']


class ServicesCpcSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServicesCpcCode
        fields = ['cpc_code', 'cpc_desc', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta',
                  'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']


class ServicesUnspscSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServicesUnspscCode
        fields = ['unspsc_code', 'unspsc_code_desc', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta',
                  'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']


'''
Limited Tendering Reasons
'''
class TenderingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TenderingReason
        fields = ['desc_en', 'desc_fr']


'''
Trade Agreement Exceptions
'''
class TAExceptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TAException
        fields = ['desc_en', 'desc_fr']


'''
CFTA Exceptions
'''
class CftaExceptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CftaException
        fields = ['desc_en', 'desc_fr']


'''
Federal Entities
'''
class FederalEntitiesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FederalEntities
        fields = ['name_en, name_fr']