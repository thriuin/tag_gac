from django.shortcuts import render, redirect
from guide.models import Code, GeneralException, CftaException, LimitedTenderingReason, Organization, CommodityType
from guide.forms import RequiredFieldsForm, GeneralExceptionForm, LimitedTenderingForm, CftaExceptionForm
from formtools.wizard.views import NamedUrlCookieWizardView
from django.http import HttpResponse
from guide.logic import FORMS, TEMPLATES, url_name, done_step_name, organization_rule, value_threshold_rule, code_rule, exceptions_rule, render_to_pdf
from django.db.models import Q
from dal import autocomplete
from django.views.generic.edit import FormView
from django.views.generic import View
from collections import OrderedDict
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date
from django.utils import translation
from guide.models import AGREEMENTS, AGREEMENTS_FIELDS

def replace_none_with_string(func_dict):
    func_replace_dict = {k:['None'] if not v else v for k,v in func_dict.items()}
    return func_replace_dict
    
def determine_final_coverage(_agreement):
    cxt = {}
    for k in _agreement.keys():
        if all(_agreement[k].values()):
            cxt[k] = True
        else:
            cxt[k] = False
    return cxt

def create_data_dict(self, forms):
    func_data_dict = {}
    try:
        for f in forms:
            func_data_dict.update(self.get_cleaned_data_for_step(f))
    except:
        pass
    return func_data_dict

def create_agreement_dict():
    func_agreement_dict = {k:{} for k in AGREEMENTS_FIELDS}
    return func_agreement_dict



def analyze_mandatory_elements(agreement, data):
    agreement = value_threshold_rule(agreement, data)
    agreement = organization_rule(agreement, data)
    agreement = code_rule(agreement, data)
    return agreement

class OpenPDF(View):
    def get(self, request, *args, **kwargs):
        
        data_dict = {}
        try:
            data_dict.update(self.request.session)
        except:
            pass
        data_dict = replace_none_with_string(data_dict)
        agreement_dict = create_agreement_dict(data_dict)

        agreement_dict = analyze_mandatory_elements(agreement_dict, data_dict)
        
        exception_dict = {
            'exceptions': GeneralException,
            'cfta_exceptions': CftaException,
        }
        agreement_dict = exceptions_rule(agreement_dict, data_dict, exception_dict)
        
        coverage_dict = determine_final_coverage(agreement_dict)
        
        data_dict['ta'] = agreement_dict
        data_dict['bool'] = coverage_dict

        number_of_ta = sum(coverage_dict.values())
        if number_of_ta == 0:
            output = 'No trade agreements apply.  '
        else:
            output = ''
            for k, v in data_dict['bool'].items():
                if number_of_ta == 1:
                    if v is True:
                        output = k.upper() + ', '
                else:
                    if v is True:
                        output = output + k.upper() + ', '
        data_dict['output'] = output[:-2]

        data_dict['tables'] = {}
        for k1, v1 in data_dict['ta'].items():
            k1 = k1.upper()
            data_dict['tables'][k1] = {}
            for k2, v2 in v1.items():
                if k1 == 'CFTA':
                    if k2 == 'type' or k2 == 'limited_tendering':
                        pass
                    else:
                        k2 = k2.replace('_', ' ')
                        k2 = k2.title()
                        k2 = k2.replace('Cfta Exceptions', 'CFTA Exceptions')
                        data_dict['tables'][k1][k2] = v2
                else:
                    if k2 == 'type' or k2 == 'limited_tendering' or k2 == 'cfta_exceptions':
                        pass
                    else:
                        k2 = k2.replace('_', ' ')
                        k2 = k2.title()
                        data_dict['tables'][k1][k2] = v2

        pdf = render_to_pdf('pdf.html', data_dict)
        return HttpResponse(pdf, content_type='application/pdf')


class CodeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        type = self.forwarded.get('type', None)
        qs = Code.objects.none()
        if type:
            value = CommodityType.objects.filter(id=type).get()
            qs = Code.objects.filter(type=value).all()
            if self.q:
                qs = Code.objects.filter(type=value).filter(code__icontains=self.q)
        return qs
        
class EntitiesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Organization.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class TypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CommodityType.objects.all()

        if self.q:
            qs = qs.filter(commodity_type__icontains=self.q)
        
        return qs

def lt_condition(wizard):
    lt_list = [f[0] for f in FORMS[:3]]

    data_dict = {}
    try:
        for f in lt_list:
            data_dict.update(wizard.get_cleaned_data_for_step(f))
    except:
        return True
    
    agreement_dict = create_agreement_dict()

    agreement_dict = analyze_mandatory_elements(agreement_dict, data_dict)
    exception_dict = {
            'exceptions': GeneralException,
            'cfta_exceptions': CftaException,
        }
    agreement_dict = exceptions_rule(agreement_dict, data_dict, exception_dict)
    
    coverage_dict = determine_final_coverage(agreement_dict)
    
    if sum(coverage_dict.values()) == 0:
        return False
    return True


class TradeForm(NamedUrlCookieWizardView):
    """
    This form wizard goes through each each form and template.

    **Context**

    Forms
        MandatoryElementsEN
            Uses these models
                :model:`guide.ValueThreshold`
                :model:`guide.Entities`
                :model:`guide.Code`
            Uses this template
                :template:'guide.mandatory_elements.html'
        
        ExceptionsEN
            Uses these models
                :model:`guide.TAExceptions`
            Uses this template
                :model:`guide.exceptions.html`
        
        CftaExceptionsEN
            Uses these models:
                :model:`guide.CftaExceptions`
            Uses this template:
                :model:`guide.cfta_exceptions.html`
    """

    form_list = [f[1] for f in FORMS]
    url_name=url_name
    done_step_name=done_step_name

    def get_template_names(self):
        """Takes the dictionary of template names defined above and returns them for the current step

        Returns:
            html file -- Returns html file for form with right template
        """
        form = [TEMPLATES[self.steps.current]]
        return form


    def get_form(self, step=None, data=None, files=None):
        form = super(TradeForm, self).get_form(step, data, files)
        
        if 'limited_tendering' in form.fields:
            lt_list = [f[0] for f in FORMS[:3]]
            data_dict = create_data_dict(self, lt_list)
            agreement_dict = create_agreement_dict()

            agreement_dict = analyze_mandatory_elements(agreement_dict, data_dict)
            exception_dict = {
                'exceptions': GeneralException,
                'cfta_exceptions': CftaException,
            }
            agreement_dict = exceptions_rule(agreement_dict, data_dict, exception_dict)
            
            coverage_dict = determine_final_coverage(agreement_dict)

            ta_applies = [k for k,v in coverage_dict.items() if v is True]

            query_list = []
            if ta_applies:
                qs = LimitedTenderingReason.objects.all()
                for ta in ta_applies:
                    field_name = ta
                    qs = qs.filter(**{field_name: True}).values_list('name')
                qs = [q[0] for q in qs]
                for q in qs:
                    query_list.append(q)
            form.fields['limited_tendering'].queryset = LimitedTenderingReason.objects.filter(name__in=query_list).only('name')
            
        return form

    def done(self, form_list, form_dict, **kwargs):
        """This function outputs the parameters for the final page done.html

        Arguments:
            form_list {list} -- list of all the forms
            form_dict {dictionary} -- list of user submitted values for each form

        Returns:
            [html] -- Renders done.html with the context that will display the
        """
        done_list = [f[0] for f in FORMS]
        data_dict = create_data_dict(self, done_list)
        agreement_dict = create_agreement_dict()

        agreement_dict = analyze_mandatory_elements(agreement_dict, data_dict)
        exception_dict = {
            'exceptions': GeneralException,
            'cfta_exceptions': CftaException,
        }
        agreement_dict = exceptions_rule(agreement_dict, data_dict, exception_dict)
        data_dict = replace_none_with_string(data_dict)
        
        data_dict['ta'] = agreement_dict
        data_dict['bool'] = determine_final_coverage(agreement_dict)

        number_of_ta = sum(data_dict['bool'].values())
        if number_of_ta == 0:
            output = 'No trade agreements apply.  '
        else:
            output = ''
            for k, v in data_dict['bool'].items():
                if number_of_ta == 1:
                    if v is True:
                        output = k.upper() + ', '
                else:
                    if v is True:
                        output = output + k.upper() + ', '
        data_dict['output'] = output[:-2]

        data_dict['tables'] = {}
        for k1, v1 in data_dict['ta'].items():
            k1 = k1.upper()
            data_dict['tables'][k1] = {}
            for k2, v2 in v1.items():
                if k1 == 'CFTA':
                    if k2 == 'type' or k2 == 'limited_tendering':
                        pass
                    else:
                        k2 = k2.replace('_', ' ')
                        k2 = k2.title()
                        k2 = k2.replace('Cfta Exceptions', 'CFTA Exceptions')
                        data_dict['tables'][k1][k2] = v2
                else:
                    if k2 == 'type' or k2 == 'limited_tendering' or k2 == 'cfta_exceptions':
                        pass
                    else:
                        k2 = k2.replace('_', ' ')
                        k2 = k2.title()
                        data_dict['tables'][k1][k2] = v2

        def add_sessions_list(name, model):
            ex_list = []
            v = data_dict[name]
            for ex in v:
                if ex != 'None':
                    check = model.objects.filter(name=ex).values_list('name').get()[0]
                else:
                    check = 'None'
                ex_list.append(check)
            self.request.session[name] = ex_list

        add_sessions_list('exceptions', GeneralException)
        add_sessions_list('cfta_exceptions', CftaException)
        for k in data_dict.keys():
            if k == 'limited_tendering':
                add_sessions_list('limited_tendering', LimitedTenderingReason)
        self.request.session['entities'] = str(data_dict['entities'])
        self.request.session['estimated_value'] = int(data_dict['estimated_value'])
        self.request.session['type'] = str(data_dict['type'])
        self.request.session['code'] = str(data_dict['code'])
        return render(self.request, 'done.html', data_dict)
