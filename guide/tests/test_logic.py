from guide.logic import FORMS, AGREEMENTS, build_context_dict, process_form, check_if_trade_agreement_applies, determine_final_coverage, organization_rule, value_threshold_rule, code_rule, exceptions_rule
from guide.models import Organization, CommodityType, Code, ValueThreshold, LimitedTenderingReason, GeneralException, CftaException, BooleanTradeAgreement, NumericTradeAgreement, Language
from guide.forms import RequiredFieldsForm, GeneralExceptionForm, CftaExceptionForm, LimitedTenderingForm
from django.test import TestCase
import unittest


class LogicTests(TestCase):
    fixtures = ['db.json']

    def test_build_context_dict(self):
        cxt = build_context_dict()
        self.assertIsInstance(cxt, dict)
        for ta in AGREEMENTS:
            self.assertIn(ta, cxt['ta'])
        
    def add_data(self):

        rf_data = {'estimated_value': 1000, 'entities': Organization.objects.get(id=1).pk, 'type': CommodityType.objects.get(id=1), 'code': Code.objects.get(id=1)}
        ge_data = {'exceptions': [GeneralException.objects.get(id=1)]}
        ce_data = {'cfta_exceptions': [CftaException.objects.get(id=1)]}
        lt_data = {'limited_tendering': [LimitedTenderingReason.objects.get(id=1)]}

        rf = RequiredFieldsForm(data=rf_data)
        ge = GeneralExceptionForm(data=ge_data)
        ce = CftaExceptionForm(data=ce_data)
        lt = LimitedTenderingForm(data=lt_data)

        rf.is_valid()
        ge.is_valid()
        ce.is_valid()
        lt.is_valid()

        return rf, ge, ce, lt

    def test_process_form(self):
        rf, ge, ce, lt = self.add_data()
        cxt = build_context_dict()

        all_data = {}
        all_data.update(rf.cleaned_data)
        all_data.update(ge.cleaned_data)
        all_data.update(ce.cleaned_data)
        all_data.update(lt.cleaned_data)

        form_list = [rf, ge, ce, lt]
        for form in form_list:
            cxt = process_form(cxt, form.cleaned_data)

        self.assertIsInstance(cxt, dict)
        self.assertTrue(all_data.items() <= cxt.items())

        for ta in AGREEMENTS:
            self.assertTrue(all_data.keys() <= cxt['ta'][ta].keys())
            self.assertNotIn(False, cxt['ta'][ta].values())
            self.assertIn(True, cxt['ta'][ta].values())
            for val in cxt['ta'][ta].values():
                self.assertTrue(val is True)
            self.assertIn(ta, cxt['ta'])

    def test_check_if_trade_agreement_applies(self):
        cxt = build_context_dict()

        rf_data = {'estimated_value': 1000, 'entities': Organization.objects.get(id=1).pk, 'type': CommodityType.objects.get(id=1), 'code': Code.objects.get(id=1)}
        ge_data = {'exceptions': [GeneralException.objects.get(id=1)]}
        ce_data = {'cfta_exceptions': [CftaException.objects.get(id=1)]}
        lt_data = {'limited_tendering': [LimitedTenderingReason.objects.get(id=1)]}

        rf = RequiredFieldsForm(data=rf_data)
        ge = GeneralExceptionForm(data=ge_data)
        ce = CftaExceptionForm(data=ce_data)
        lt = LimitedTenderingForm(data=lt_data)

        rf.is_valid()
        ge.is_valid()
        ce.is_valid()
        lt.is_valid()

        all_data = {}
        all_data.update(rf.cleaned_data)
        all_data.update(ge.cleaned_data)
        all_data.update(ce.cleaned_data)
        all_data.update(lt.cleaned_data)

        form_list = [rf, ge, ce, lt]
        for form in form_list:
            cxt = process_form(cxt, form.cleaned_data)
            
        code_name='code'
        value = cxt[code_name]
        data = Code.objects.filter(code=value)
        for ta in cxt['ta']:
            cxt = check_if_trade_agreement_applies(ta, cxt, data, code_name)

        self.assertIsInstance(cxt, dict)
        self.assertTrue(all_data.items() <= cxt.items())


