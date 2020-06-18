from django.test import TestCase
from guide.models import Organization, CommodityType, Code, ValueThreshold, LimitedTenderingReason, GeneralException, CftaException, BooleanTradeAgreement, NumericTradeAgreement, Language
from guide.logic import FORMS, TEMPLATES, agreements, url_name, done_step_name, determine_final_coverage, organization_rule, value_threshold_rule, code_rule, exceptions_rule, build_context_dict, process_form
import unittest


class UrlsTest(TestCase):
    def test_mandatory_elements(self):
        resp = self.client.get('/tag/0/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'mandatory_elements.html')

    def test_general_exceptions(self):
        resp = self.client.get('/tag/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'exceptions.html')
    
    def test_cfta_exceptions(self):
        resp = self.client.get('/tag/2/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cfta_exceptions.html')

    def test_limited_tendering_redirect(self):
        resp = self.client.get('/tag/3/')
        self.assertRedirects(resp, '/tag/0/', status_code=302)

    def test_done_step_redirect(self):
        resp = self.client.get('/tag/done_step/')
        self.assertRedirects(resp, '/tag/0/', status_code=302)

    def test_redirect_tag_gac_one(self):
        resp = self.client.get('/')
        self.assertRedirects(resp, '/tag/0/', status_code=301)

    def test_redirect_tag_gac_two(self):
        resp = self.client.get('/anytext/')
        self.assertRedirects(resp, '/tag/0/', status_code=301)

    def test_redirect_guide_one(self):
        resp = self.client.get('/tag')
        self.assertRedirects(resp, '/tag/0/', status_code=301)

    def test_redirect_guide_two(self):
        resp = self.client.get('/tag/anytext')
        self.assertRedirects(resp, '/tag/0/', status_code=301)