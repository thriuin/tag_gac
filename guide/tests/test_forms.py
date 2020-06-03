from django.test import TestCase
from guide.models import Organization, CommodityType, Code, ValueThreshold, TenderingReason, GeneralException, CftaException, BooleanTradeAgreement, NumericTradeAgreement, Language
from guide.logic import FORMS, TEMPLATES, agreements, url_name, done_step_name, determine_final_coverage, organization_rule, value_threshold_rule, code_rule, exceptions_rule, build_context_dict, process_form
import unittest
from guide.forms import RequiredFieldsFormEN, GeneralExceptionFormEN, CftaExceptionFormEN, LimitedTenderingFormEN, estimated_value_label, entities_label, type_label, code_label, general_exceptions_label, cfta_exceptions_label, limited_tendering_label
from django import forms, http
from django.core.exceptions import ValidationError
from django.conf import settings
from django.template.response import TemplateResponse
from guide.views import TradeForm
from importlib import import_module
from guide.logic import FORMS, TEMPLATES, url_name, done_step_name
from guide.urls import trade_wizard
from formtools.wizard.views import NamedUrlSessionWizardView, WizardView


class FormsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Organization.objects.create(name='Model Ministry', lang='EN')
        CommodityType.objects.create(commodity_type='Model Commodity Type', lang='EN')
        Code.objects.create(code='ZZZ Model Commodity Code', type=CommodityType.objects.get(id=1), lang='EN')
        ValueThreshold.objects.create(type_value=CommodityType.objects.get(id=1))
        TenderingReason.objects.create(name='Model Limited Tendering Reason', lang='EN')
        GeneralException.objects.create(name='Model General Exception', lang='EN')
        CftaException.objects.create(name='Model CFTA Exception', lang='EN')

    def test_required_fields_labels(self):
        form = RequiredFieldsFormEN()
        self.assertIn(str(estimated_value_label), form.as_p())
        self.assertIn(str(entities_label), form.as_p())
        self.assertIn(str(type_label), form.as_p())
        self.assertIn(str(code_label), form.as_p())

    def test_general_exceptions_label(self):
        form = GeneralExceptionFormEN()
        self.assertIn(str(general_exceptions_label), form.as_p())
        
    def test_cfta_exceptions_label(self):
        form = CftaExceptionFormEN()
        self.assertIn(str(cfta_exceptions_label), form.as_p())
    
    def test_limited_tendering_label(self):
        form = LimitedTenderingFormEN()
        self.assertIn(str(limited_tendering_label), form.as_p())

    def test_required_fields_blank(self):
        form = RequiredFieldsFormEN(data={'estimated_value': None, 'entities': '', 'type': '', 'code': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['estimated_value'], ['This field is required.'])
        self.assertEqual(form.errors['entities'], ['This field is required.'])
        self.assertEqual(form.errors['type'], ['This field is required.'])
        self.assertEqual(form.errors['code'], ['This field is required.'])

    def test_required_fields_wrong_data_one(self):
        form = RequiredFieldsFormEN(data={'estimated_value': -1, 'entities': 'Missing dept', 'type': 'missing type', 'code': 'missing code'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['estimated_value'], ['Ensure this value is greater than or equal to 0.'])
        self.assertEqual(form.errors['entities'], ['Select a valid choice. That choice is not one of the available choices.'])
        self.assertEqual(form.errors['type'], ['Select a valid choice. That choice is not one of the available choices.'])
        self.assertEqual(form.errors['code'], ['Select a valid choice. That choice is not one of the available choices.'])

    def test_required_fields_wrong_data_two(self):
        form = RequiredFieldsFormEN(data={'estimated_value': 'dsfdsf', 'entities': 'Missing dept', 'type': 'missing type', 'code': 'missing code'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['estimated_value'], ['Enter a whole number.'])
        self.assertEqual(form.errors['entities'], ['Select a valid choice. That choice is not one of the available choices.'])
        self.assertEqual(form.errors['type'], ['Select a valid choice. That choice is not one of the available choices.'])
        self.assertEqual(form.errors['code'], ['Select a valid choice. That choice is not one of the available choices.'])

    def test_required_fields_valid_data(self):
        form = RequiredFieldsFormEN(data={'estimated_value': 1000, 'entities': Organization.objects.get(id=1).pk, 'type': CommodityType.objects.get(id=1), 'code': Code.objects.get(id=1)})
        self.assertTrue(form.is_valid())

    def test_general_exceptions_blank(self):
        form = GeneralExceptionFormEN(data={'exceptions': ''})
        self.assertTrue(form.is_valid())

    def test_general_exceptions_wrong(self):
        form = GeneralExceptionFormEN(data={'exceptions': ['missing exception']})
        self.assertFalse(form.is_valid())

    def test_general_exceptions_valid(self):
        form = GeneralExceptionFormEN(data={'exceptions': [GeneralException.objects.get(id=1)]})
        self.assertTrue(form.is_valid())

    def test_cfta_exceptions_blank(self):
        form = CftaExceptionFormEN(data={'cfta_exceptions': ''})
        self.assertTrue(form.is_valid())
    
    def test_cfta_exceptions_wrong(self):
        form = CftaExceptionFormEN(data={'cfta_exceptions': ['missing exception']})
        self.assertFalse(form.is_valid())
    
    def test_cfta_exceptions_valid(self):
        form = CftaExceptionFormEN(data={'cfta_exceptions': [CftaException.objects.get(id=1)]})
        self.assertTrue(form.is_valid())

    def test_limited_tendering_blank(self):
        form = LimitedTenderingFormEN(data={'limited_tendering': ''})
        self.assertTrue(form.is_valid())
    
    def test_limited_tendering_wrong(self):
        form = LimitedTenderingFormEN(data={'limited_tendering': 'wrong reason'})
        self.assertFalse(form.is_valid())
    
    def test_limited_tendering_valid(self):
        form = LimitedTenderingFormEN(data={'limited_tendering': [TenderingReason.objects.get(id=1)]})
        self.assertTrue(form.is_valid())