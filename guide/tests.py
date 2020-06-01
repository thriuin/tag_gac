from django.test import TestCase
from guide.models import Organization, CommodityType, Code, ValueThreshold, TenderingReason, GeneralException, CftaException, BooleanTradeAgreement, NumericTradeAgreement, Language
from django.urls import reverse
from guide.logic import FORMS, TEMPLATES, agreements, url_name, done_step_name, determine_final_coverage, organization_rule, value_threshold_rule, code_rule, exceptions_rule, build_context_dict, process_form
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import time
from selenium.webdriver.support.ui import Select
import unittest

# models tests
class ModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Organization.objects.create(name='Model Ministry')
        CommodityType.objects.create(commodity_type='Model Commodity Type')
        Code.objects.create(code='ZZZ Model Commodity Code', type=CommodityType.objects.get(id=1))
        ValueThreshold.objects.create(type_value=CommodityType.objects.get(id=1))
        TenderingReason.objects.create(name='Model Limited Tendering Reason')
        GeneralException.objects.create(name='Model General Exception')
        CftaException.objects.create(name='Model CFTA Exception')
    @unittest.skip('none')
    def test_organization(self):
        label = Organization.objects.get(id=1)
        self.assertEqual(str(label), label.__str__())
        self.assertTrue(isinstance(label, Organization))
    @unittest.skip('none')
    def test_commodity_type(self):
        label = CommodityType.objects.get(id=1)
        self.assertEqual(str(label), label.__str__())
        self.assertTrue(isinstance(label, CommodityType))
    @unittest.skip('none')
    def test_code(self):
        label = Code.objects.get(id=1)
        self.assertEqual(str(label), label.__str__())
        self.assertTrue(isinstance(label, Code))
    @unittest.skip('none')
    def test_value_threshold(self):
        label = ValueThreshold.objects.get(id=1)
        self.assertEqual(str(label), label.__str__())
        self.assertTrue(isinstance(label, ValueThreshold))
    @unittest.skip('none')
    def test_tendering_reason(self):
        label = TenderingReason.objects.get(id=1)
        self.assertEqual(str(label), label.__str__())
        self.assertTrue(label, TenderingReason)
    @unittest.skip('none')
    def test_general_exception(self):
        label = GeneralException.objects.get(id=1)
        self.assertEqual(str(label), label.__str__())
        self.assertTrue(label, GeneralException)
    @unittest.skip('none')
    def test_cfta_exception(self):
        label = CftaException.objects.get(id=1)
        self.assertEqual(str(label), label.__str__())    
        self.assertTrue(label, CftaException)


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        Organization.objects.create(name='Model Ministry')
        CommodityType.objects.create(commodity_type='Model Commodity Type')
        Code.objects.create(code='ZZZ Model Commodity Code', type=CommodityType.objects.get(id=1))
        ValueThreshold.objects.create(type_value=CommodityType.objects.get(id=1))
        TenderingReason.objects.create(name='Model Limited Tendering Reason')
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
    @unittest.skip('none')
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

commodity_type_list = {'Goods', 'Services', 'Construction'}
commodity_code_default = Code.objects.filter(type='Goods').values_list('code')[1]

def step_through_form(self, estimated_value=1000000000, organization=None, commodity_type='Goods', 
                            general_exception=None, cfta_exception=None, lt_page=True, limited_tendering_reason=None):
    self.selenium.get(self.live_server_url + '/en/tag/0/')

    if estimated_value < 0:
        raise ValueError('Estimated value cannot be less than zero')

    # Mandatory elements page
    try:
        estimated_value_input = self.selenium.find_element_by_name("0-estimated_value")
        org_input = Select(self.selenium.find_element_by_name("0-entities"))
        type_input = Select(self.selenium.find_element_by_name("0-type"))
        code_input = Select(self.selenium.find_element_by_name("0-code"))
    except:
        raise Exception('Cannot find elements in mandatory elements page')

    estimated_value_input.send_keys(estimated_value)
    
    if organization:
        valid_orgs = Organization.objects.values_list('name')
        if organization not in valid_orgs:
            raise ValueError('Organization not in model')
        org = organization
    else:
        org = Organization.objects.filter(tc=False).\
                filter(goods_rule=False).filter(cusma=True).\
                filter(ccfta=True).filter(ccofta=True).\
                filter(chfta=True).filter(cpafta=True).\
                filter(cpfta=True).filter(ckfta=True).\
                filter(cufta=True).filter(wto_agp=True).\
                filter(ceta=True).filter(cptpp=True).\
                filter(cfta=True).values_list('name')[0]

    org_input.select_by_visible_text(org)

    type_input.select_by_visible_text(commodity_type)

    value = Code.objects.filter(type=commodity_type).values_list('code')[1]
    code_input.select_by_visible_text(value)
    
    time.sleep(1)
    self.selenium.find_element_by_xpath('//input[@value="Next"]').click()

    def checklist(element):
        time.sleep(1)
        if element:
            element=element[0]
            try:
                check = self.selenium.find_element_by_xpath(".//div[@class='checkbox']/span/label[contains(., '" + element + "')]/input")
                check.click()
            except:
                raise Exception('Cannot find ' + element)

        self.selenium.find_element_by_xpath('//input[@value="Next"]').click()

    checklist(general_exception)
    checklist(cfta_exception)
    
    if lt_page:
        checklist(limited_tendering_reason)

    output = self.selenium.find_element_by_id('output').text
    return output    

class SeleniumTests(StaticLiveServerTestCase):
    port = 8000
    fixtures = ["guide/fixtures/db.json"]

    wizard_urlname = url_name

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    @unittest.skip('none')
    def test_all_apply(self):
        output = step_through_form(self)
        
        for ta in agreements:
            self.assertIn(ta.upper(), output)
    @unittest.skip('none')
    def test_low_estimated_value(self):
        output = step_through_form(self, estimated_value=1, lt_page=False)

        for ta in agreements:
            self.assertNotIn(ta.upper(), output)
    
    #Entity none apply
    @unittest.skip('none')
    def test_org_none_apply(self):
        org = Organization.objects.filter(tc=False).\
            filter(goods_rule=False).filter(cusma=False).\
            filter(ccfta=False).filter(ccofta=False).\
            filter(chfta=False).filter(cpafta=False).\
            filter(cpfta=False).filter(ckfta=False).\
            filter(cufta=False).filter(wto_agp=False).\
            filter(ceta=False).filter(cptpp=False).\
            filter(cfta=False).values_list('name')[0]

        output = step_through_form(self, organization=org, lt_page=False)
        for ta in agreements:
            self.assertNotIn(ta.upper(), output)
    @unittest.skip('none')
    def test_goods_rule(self):
        org = Organization.objects.filter(goods_rule=True).values_list('name')[0]

        output = step_through_form(self, organization=org)
        agmt = agreements
        agmt.remove('cfta')

        self.assertIn('CFTA', output)
        for ta in agmt:
            self.assertNotIn(ta.upper(), output)
    @unittest.skip('none')
    def test_tc_rule(self):
        org = Organization.objects.filter(tc=True).values_list('name')[0]
        output = step_through_form(self, organization=org, commodity_type='Construction')

        agmt = agreements
        agmt.remove('cfta')

        self.assertIn('CFTA', output)
        for ta in agmt:
            self.assertNotIn(ta.upper(), output)
    @unittest.skip('none')
    def test_general_exception_cfta_applies(self):
        ge = GeneralException.objects.filter(cusma=True).\
            filter(ccfta=True).filter(ccofta=True).\
            filter(chfta=True).filter(cpafta=True).\
            filter(cpfta=True).filter(ckfta=True).\
            filter(cufta=True).filter(wto_agp=True).\
            filter(ceta=True).filter(cptpp=True).\
            filter(cfta=False).values_list('name')[0]
        output = step_through_form(self, general_exception=ge)

        agmt = agreements
        agmt.remove('cfta')

        self.assertIn('CFTA', output)
        for ta in agmt:
            self.assertNotIn(ta.upper(), output)

    def test_general_exception_none_applies(self):
        ge = GeneralException.objects.filter(cusma=True).\
            filter(ccfta=True).filter(ccofta=True).\
            filter(chfta=True).filter(cpafta=True).\
            filter(cpfta=True).filter(ckfta=True).\
            filter(cufta=True).filter(wto_agp=True).\
            filter(ceta=True).filter(cptpp=True).\
            filter(cfta=True).values_list('name')[0]
        output = step_through_form(self, general_exception=ge, lt_page=False)

        for ta in agreements:
            self.assertNotIn(ta.upper(), output)