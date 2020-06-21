from django.shortcuts import render
from guide.models import Code, GeneralException, CftaException, LimitedTenderingReason
from guide.forms import RequiredFieldsForm, GeneralExceptionForm, LimitedTenderingForm, CftaExceptionForm
from formtools.wizard.views import NamedUrlSessionWizardView
from django.http import JsonResponse
from guide.logic import FORMS, TEMPLATES, agreements, url_name, done_step_name, determine_final_coverage, organization_rule, value_threshold_rule, code_rule, exceptions_rule, build_context_dict, process_form
from django.db.models import Q

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
                for ta in ta_applies:
                    field_name = ta
                    qs = LimitedTenderingReason.objects.filter(**{field_name: True}).values_list('name')
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


def ajax_type(request):
    """
    This view is triggered by changing Commodity Type in the MandatoryElementsEn form.
    get all the types from the database
    null and blank values
    
    **Context**

    Uses this model
        :model:`guide.Code`
    Uses this template
        :template:`guide.mandatory_elements.html`
    """
    if request.method == "GET" and request.is_ajax():
        if request.LANGUAGE_CODE == 'en-ca':
            type_en_ca = Code.objects.\
                exclude(type_en_ca__isnull=True).\
                exclude(type_en_ca__exact='').\
                order_by('type_en_ca').\
                values_list('type_en_ca').\
                distinct()
            type_en_ca = [i[0] for i in list(type_en_ca)]
            data = {
                "type": type_en_ca,
            }
            return JsonResponse(data, status = 200)
        else:
            type_fr_ca = Code.objects.\
                exclude(type_fr_ca__isnull=True).\
                exclude(type_fr_ca__exact='').\
                order_by('type_fr_ca').\
                values_list('type_fr_ca').\
                distinct()
            type_fr_ca = [i[0] for i in list(type_fr_ca)]
            data = {
                "type": type_fr_ca,
            }
            return JsonResponse(data, status = 200)


def ajax_code(request):
    """
    This view is triggered by changing Commodity Type in the MandatoryElementsEn form.
    get the type and filter to get code
    database excluding null and blank values
    
    **Context**

    Uses this models
        :model:`guide.Code`
    Uses this template
        :template:`guide.mandatory_elements.html`
    """
    if request.method == "GET" and request.is_ajax():
        type = request.GET.get('type')
        if request.LANGUAGE_CODE == 'en-ca':
            code = Code.objects.\
                filter(type_en_ca = type).\
                exclude(code__isnull=True).\
                exclude(code__exact='').\
                values_list('code').\
                distinct()
            code = [i[0] for i in list(code)]
            data = {
                "code": code,
            }
            return JsonResponse(data, status = 200)

