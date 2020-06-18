from django.test import TestCase
from guide.models import Organization, CommodityType, Code, ValueThreshold, LimitedTenderingReason, GeneralException, CftaException, BooleanTradeAgreement, NumericTradeAgreement, Language
from django.urls import reverse
from guide.logic import FORMS, TEMPLATES, agreements, url_name, done_step_name, determine_final_coverage, organization_rule, value_threshold_rule, code_rule, exceptions_rule, build_context_dict, process_form
import unittest


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        Organization.objects.create(name='Model Ministry')
        CommodityType.objects.create(commodity_type='Model Commodity Type')
        Code.objects.create(code='ZZZ Model Commodity Code', type=CommodityType.objects.get(id=1))
        ValueThreshold.objects.create(type_value=CommodityType.objects.get(id=1))
        LimitedTenderingReason.objects.create(name='Model Limited Tendering Reason')
        GeneralException.objects.create(name='Model General Exception')
        CftaException.objects.create(name='Model CFTA Exception')


    wizard_urlname = url_name
    wizard_step_1_data = {
        'trade_wizard-current_step': '0',
    }
    wizard_step_data = (
        {
            'estimated_value': 1000,
            'entities': 'Model Ministry',
            'type': 'Model Commodity Type',
            'code': 'ZZZ Model Commodity Code',
            'trade_wizard-current_step': '0',
        },
        {
            'exceptions': ['Model General Exception'],
            'trade_wizard-current_step': '1',
        },
        {
            'cfta_exceptions': ['Model CFTA Exception'],
            'trade_wizard-current_step': '2',
        },
        {
            'limited_tendering': ['Model Limited Tendering Reason'],
            'trade_wizard-current_step': '3',
        }
    )
    
    def test_initial_call(self):
        response = self.client.get(reverse(self.wizard_urlname, args=['0']))
        self.assertEqual(response.status_code, 200)
        wizard = response.context['wizard']
        self.assertEqual(wizard['steps'].current, '0')
        self.assertEqual(wizard['steps'].step0, 0)
        self.assertEqual(wizard['steps'].step1, 1)
        self.assertEqual(wizard['steps'].last, '2')
        self.assertEqual(wizard['steps'].prev, None)
        self.assertEqual(wizard['steps'].next, '1')
        self.assertEqual(wizard['steps'].count, 3)
        self.assertEqual(wizard['url_name'], self.wizard_urlname)
