from django.test import TestCase
from guide.models import Organization, CommodityType, Code, ValueThreshold, TenderingReason, GeneralException, CftaException, BooleanTradeAgreement, NumericTradeAgreement, Language
from django.urls import reverse
from guide.logic import FORMS, TEMPLATES, agreements, url_name, done_step_name, determine_final_coverage, organization_rule, value_threshold_rule, code_rule, exceptions_rule, build_context_dict, process_form
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import time
from selenium.webdriver.support.ui import Select

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

    def test_organization(self):
        label = Organization.objects.get(id=1)
        self.assertEqual(str(label), label.__str__())
        self.assertTrue(isinstance(label, Organization))

    def test_commodity_type(self):
        label = CommodityType.objects.get(id=1)
        self.assertEqual(str(label), label.__str__())
        self.assertTrue(isinstance(label, CommodityType))

    def test_code(self):
        label = Code.objects.get(id=1)
        self.assertEqual(str(label), label.__str__())
        self.assertTrue(isinstance(label, Code))

    def test_value_threshold(self):
        label = ValueThreshold.objects.get(id=1)
        self.assertEqual(str(label), label.__str__())
        self.assertTrue(isinstance(label, ValueThreshold))

    def test_tendering_reason(self):
        label = TenderingReason.objects.get(id=1)
        self.assertEqual(str(label), label.__str__())
        self.assertTrue(label, TenderingReason)

    def test_general_exception(self):
        label = GeneralException.objects.get(id=1)
        self.assertEqual(str(label), label.__str__())
        self.assertTrue(label, GeneralException)

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

entities_list = {'default', 'tc', 'goods_rule'}
commodity_type_list = {'Goods', 'Services', 'Construction'}
commodity_code_default = Code.objects.filter(type='Goods').values_list('code')[1]

def step_through_form(self, estimated_value=1000000000, entities='default', commodity_type='Goods', 
                            general_exception=None, cfta_exception=None, lt_page=True, limited_tendering_reason=None):
    self.selenium.get(self.live_server_url + '/en/tag/0/')

    # Mandatory elements page
    try:
        estimated_value_input = self.selenium.find_element_by_name("0-estimated_value")
        entities_input = Select(self.selenium.find_element_by_name("0-entities"))
        type_input = Select(self.selenium.find_element_by_name("0-type"))
        code_input = Select(self.selenium.find_element_by_name("0-code"))
    except:
        raise Exception('Cannot find elements in mandatory elements page')

    estimated_value_input.send_keys(estimated_value)
    
    org = Organization.objects.filter(tc=False).values_list('name')[0]
    entities_input.select_by_visible_text(org)

    type_input.select_by_visible_text(commodity_type)

    value = Code.objects.filter(type=commodity_type).values_list('code')[1]
    code_input.select_by_visible_text(value)
    
    time.sleep(1)
    self.selenium.find_element_by_xpath('//input[@value="Next"]').click()

    def checklist(element):
        time.sleep(1)
        if element:
            try: 
                check = self.selenium.find_element_by_id(element)
                check.click()
            except:
                raise Exception('Cannot find ' + element)

        self.selenium.find_element_by_xpath('//input[@value="Next"]').click()

    checklist(general_exception)
    checklist(cfta_exception)
    
    if lt_page:
        checklist(limited_tendering_reason)

    

class SeleniumTests(StaticLiveServerTestCase):
    port = 8000
    fixtures = ["guide/fixtures/db.json"]

    wizard_urlname = url_name

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_form_1(self):
        t = step_through_form(self)

        