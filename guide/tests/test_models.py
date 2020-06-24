from django.test import TestCase
from guide.models import Organization, CommodityType, Code, ValueThreshold, LimitedTenderingReason, GeneralException, CftaException, BooleanTradeAgreement, NumericTradeAgreement, Language
from guide.logic import FORMS, TEMPLATES, AGREEMENTS, url_name, done_step_name, determine_final_coverage, organization_rule, value_threshold_rule, code_rule, exceptions_rule, build_context_dict, process_form
import unittest

# models tests

class ModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Organization.objects.create(name='Model Ministry')
        CommodityType.objects.create(commodity_type='Model Commodity Type')
        Code.objects.create(code='ZZZ Model Commodity Code', type=CommodityType.objects.get(id=1))
        ValueThreshold.objects.create(type_value=CommodityType.objects.get(id=1))
        LimitedTenderingReason.objects.create(name='Model Limited Tendering Reason')
        GeneralException.objects.create(name='Model General Exception')
        CftaException.objects.create(name='Model CFTA Exception')
    
    def test_organization(self):
        model_string = Organization.objects.get(id=1)
        self.assertEqual(str(model_string), model_string.__str__())
        self.assertTrue(isinstance(model_string, Organization))
    
    def test_commodity_type(self):
        model_string = CommodityType.objects.get(id=1)
        self.assertEqual(str(model_string), model_string.__str__())
        self.assertTrue(isinstance(model_string, CommodityType))
    
    def test_code(self):
        model_string = Code.objects.get(id=1)
        self.assertEqual(str(model_string), model_string.__str__())
        self.assertTrue(isinstance(model_string, Code))
    
    def test_value_threshold(self):
        model_string = ValueThreshold.objects.get(id=1)
        self.assertEqual(str(model_string), model_string.__str__())
        self.assertTrue(isinstance(model_string, ValueThreshold))
   
    def test_tendering_reason(self):
        model_string = LimitedTenderingReason.objects.get(id=1)
        self.assertEqual(str(model_string), model_string.__str__())
        self.assertTrue(model_string, LimitedTenderingReason)
    
    def test_general_exception(self):
        model_string = GeneralException.objects.get(id=1)
        self.assertEqual(str(model_string), model_string.__str__())
        self.assertTrue(model_string, GeneralException)
    
    def test_cfta_exception(self):
        model_string = CftaException.objects.get(id=1)
        self.assertEqual(str(model_string), model_string.__str__())    
        self.assertTrue(model_string, CftaException)
