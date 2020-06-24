from django.shortcuts import render
from guide.models import Code, GeneralException, CftaException, LimitedTenderingReason, Organization, CommodityType
from guide.forms import RequiredFieldsForm, GeneralExceptionForm, LimitedTenderingForm, CftaExceptionForm
from formtools.wizard.views import NamedUrlSessionWizardView
from django.http import JsonResponse
from guide.logic import FORMS, TEMPLATES, AGREEMENTS, url_name, done_step_name, determine_final_coverage, organization_rule, value_threshold_rule, code_rule, exceptions_rule, build_context_dict, process_form
from django.db.models import Q
from dal import autocomplete
from django.views.generic.edit import FormView


class CodeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        type = self.forwarded.get('type', None)
        qs = Code.objects.none()
        if type:
            value = CommodityType.objects.filter(id=type).get()
            qs = Code.objects.filter(type=value).all()
            if self.q:
                qs = Code.objects.filter(type=value).filter(code__icontains=self.q)
                print('code inner ifif')

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
    form_list = [f[0] for f in FORMS[:3]]
    context_dict = build_context_dict()
    for form in form_list:
        val = wizard.get_cleaned_data_for_step(form)
        if not val:
            return False
        else:
            context_dict = process_form(context_dict, val)

    context_dict = value_threshold_rule(context_dict, 'estimated_value', 'type')
    context_dict = organization_rule(context_dict, 'entities')
    context_dict = code_rule(context_dict, 'code', 'type', 'entities')
    context_dict = exceptions_rule(context_dict, 'exceptions', GeneralException)
    context_dict = exceptions_rule(context_dict, 'cfta_exceptions', CftaException)
    context_dict = determine_final_coverage(context_dict)

    for v in context_dict['bool'].values():
        if v is True:
            return True
    return False


class TradeForm(NamedUrlSessionWizardView):
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
            form_list = [f[0] for f in FORMS[:3]]
            context_dict = build_context_dict()
            for f in form_list:
                val = self.get_cleaned_data_for_step(f)
                if not val:
                    return False
                else:
                    context_dict = process_form(context_dict, val)
            
            context_dict = value_threshold_rule(context_dict, 'estimated_value', 'type')
            context_dict = organization_rule(context_dict, 'entities')
            context_dict = code_rule(context_dict, 'code', 'type', 'entities')
            context_dict = exceptions_rule(context_dict, 'exceptions', GeneralException)
            context_dict = exceptions_rule(context_dict, 'cfta_exceptions', CftaException)
            context_dict = determine_final_coverage(context_dict)
            
            ta_applies = []
            for k, v in context_dict['bool'].items():
                if v is True:
                    ta_applies.append(k)
            
            query_list = []
            if ta_applies:
                qs = LimitedTenderingReason.objects.all()
                for ta in ta_applies:
                    field_name = ta
                    qs = qs.filter(**{field_name: True}).values_list('name')
                qs = [q[0] for q in qs]
                for q in qs:
                    query_list.append(q)
            print(query_list)
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
        context_dict = build_context_dict()

        for form in form_list:
            context_dict = process_form(context_dict, form.cleaned_data)

        context_dict = value_threshold_rule(context_dict, 'estimated_value', 'type')
        context_dict = organization_rule(context_dict, 'entities')
        context_dict = code_rule(context_dict, 'code', 'type', 'entities')
        context_dict = exceptions_rule(context_dict, 'exceptions', GeneralException)
        context_dict = exceptions_rule(context_dict, 'cfta_exceptions', CftaException)
        context_dict = determine_final_coverage(context_dict)

        num_true = sum(context_dict['bool'].values())
        
        if num_true == 0:
            output = 'No trade agreements apply.  '
        else:
            output = ''
            for k, v in context_dict['bool'].items():
                if num_true == 1:
                    if v is True:
                        output = k.upper() + ', '
                else:
                    if v is True:
                        output = output + k.upper() + ', '
        context_dict['output'] = output[:-2]

        context_dict['tables'] = {}
        for k1, v1 in context_dict['ta'].items():
            k1 = k1.upper()
            context_dict['tables'][k1] = {}
            for k2, v2 in v1.items():
                if k1 == 'CFTA':
                    if k2 == 'type' or k2 == 'limited_tendering':
                        pass
                    else:
                        k2 = k2.replace('_', ' ')
                        k2 = k2.title()
                        k2 = k2.replace('Cfta Exceptions', 'CFTA Exceptions')
                        context_dict['tables'][k1][k2] = v2
                else:
                    if k2 == 'type' or k2 == 'limited_tendering' or k2 == 'cfta_exceptions':
                        pass
                    else:
                        k2 = k2.replace('_', ' ')
                        k2 = k2.title()
                        context_dict['tables'][k1][k2] = v2
        return render(self.request, 'done.html', context_dict)
