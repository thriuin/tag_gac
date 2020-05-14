from django.shortcuts import render
from guide.models import Code, ValueThreshold, Organization, GeneralException, TenderingReason, CftaException
from guide.forms import MandatoryElementsEN, ExceptionsEN, LimitedTenderingEN, CftaExceptionsEN
from formtools.wizard.views import NamedUrlSessionWizardView
from django.http import JsonResponse

FORMS = [("0", MandatoryElementsEN),
         ("1", ExceptionsEN),
         ("2", CftaExceptionsEN),
         ("3", LimitedTenderingEN)]

TEMPLATES = {"0": "mandatory_elements.html",
             "1": "exceptions.html",
             "2": "cfta_exceptions.html",
             "3": "limited_tendering.html"}

agreements = [
    'nafta', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 
    'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta'
]

url_name='guide:form_step'
done_step_name='guide:done_step'


def entities_rule(context, org_name):
    """Checks which trade agreements apply to the selected entity

    Arguments:
        context {dictionary} -- The context keeps track of all the values submitted and the analysis
        org_name {string} -- From context this gets the submitted value

    Raises:
        ValueError: Returns value error if there is a problem with context

    Returns:
        [dictionary] -- Returns updated context dict with analysis (true or false)
    """
    org = context[org_name]
    trade_agreements = context['ta']
    try:
        for ta in trade_agreements:
            check = Organization.objects.filter(name=org).values_list(ta).get()[0]
            if check is False:
                context['ta'][ta][org_name] = False
            else:
                context['ta'][ta][org_name] = True
    except:
        raise ValueError
    return context

def value_threshold_rule(context, value_name, type_name):
    """Checks whether the value submitted by the user is less than or greater than the
    value in the trade agreement.

    Arguments:
        context {dictionary} -- The context keeps track of all the values submitted and the analysis
        col_estimated_value {string} -- From context this gets the submitted value
        col_type {string} -- From context this gets the submitted value

    Raises:
        ValueError: Output if there is an error with the context

    Returns:
        [dictionary] -- Updates context with the analyzed value, either true or false
    """
    value = context[value_name]
    type = context[type_name]
    trade_agreements = context['ta']
    try:
        for ta in trade_agreements:
            check = ValueThreshold.objects.filter(type_value=type).values_list(ta).get()[0]
            if value < check:
                context['ta'][ta][value_name] = False
            else:
                context['ta'][ta][value_name] = True
    except:
        raise ValueError
    return context

def code_rule(context, code_name, type_name, org_name):
    """Checks if the code selected by the user is covered by each trade agreement.

    Arguments:
        context {dictionary} -- Context tracks user input and analysis
        col_code {string} -- String to select user value for code from the context
        type_col {string} -- String to select user value for type from the context
        org_name {string} -- String to select user value for org from the context

    Raises:
        ValueError: If error in context

    Returns:
        [dictionary] -- Returns context with updated analysis
    """
    value = context[code_name]
    type = context[type_name]
    org = context[org_name]
    trade_agreements = context['ta']

    try:
        if type == 'Goods':
            defence_rule = Organization.objects.filter(name=org).values_list('weapons_rule').get()[0]
            for ta in trade_agreements:
                if defence_rule is False:
                    context['ta'][ta][code_name] = True
                else:
                    context['ta'][ta][code_name] = False
                return context
        elif type == 'Construction':
            tc_rule = Organization.objects.filter(name=org).values_list('tc').get()[0]
            for ta in trade_agreements:
                if tc_rule is False:
                    context['ta'][ta][code_name] = True
                else:
                    context['ta'][ta][code_name] = False
            return context
        else:
            for ta in trade_agreements:
                check = Code.objects.filter(code=value).values_list(ta).get()[0]
                if check is False:
                    context['ta'][ta][code_name] = False
                else:
                    context['ta'][ta][code_name] = True
    except:
        raise ValueError
    return context

def exceptions_rule(context, exception_name, model):
    """This function goes through the exceptions that the user selected and checks which trade agreements
    apply to each exception.  If a user selects a trade agreements and an exception applies then that
    agreement is set to False.

    Arguments:
        context {dictionary} -- Context tracks user input and analysis
        col {[type]} -- From context this gets the submitted value
        model {model} -- This gets the model related to the submitted value

    Raises:
        ValueError: If error in context

    Returns:
        Dictionary -- Returns updated context dictionary with analysis
    """
    trade_agreements = context['ta']
    if context[exception_name]:
        value = context[exception_name]
        try:
            for ta in trade_agreements:
                for ex in value:
                    check = model.objects.filter(name=ex).values_list(ta).get()[0]

                    if (context['ta'][ta][exception_name] is False):
                        pass
                    elif (context['ta'][ta][exception_name] is True) and (check is False):
                        pass
                    elif (context['ta'][ta][exception_name] is True) and (check is True):
                        context['ta'][ta][exception_name] = False
        except:
            raise ValueError
    else:
        context[exception_name]= ['None']
    return context

"""
def show_message_form_condition(wizard):
    # try to get the cleaned data of step 1
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    # check if the field ``leave_message`` was checked.
    return cleaned_data.get('leave_message', True)
"""
def lt_condition(wizard):
    form_list = [f[0] for f in FORMS[:3]]
    context_dict = {}
    trade_agreements = {ta:{} for ta in agreements}

    for form in form_list:
        val = wizard.get_cleaned_data_for_step(form)
        if not val:
            return False
        else:
            for k, v, in val.items():
                context_dict[k] = v
                for k2 in trade_agreements.keys():
                    trade_agreements[k2][k] = True
    context_dict['ta'] = trade_agreements

    context_dict = value_threshold_rule(context_dict, 'estimated_value', 'type')
    context_dict = entities_rule(context_dict, 'entities')
    context_dict = code_rule(context_dict, 'code', 'type', 'entities')
    context_dict = exceptions_rule(context_dict, 'exceptions', GeneralException)
    context_dict = exceptions_rule(context_dict, 'cfta_exceptions', CftaException)

    context_dict['bool'] = {}
    for ta in trade_agreements:
        context_dict['bool'][ta] = True
        for k, v in context_dict['ta'][ta].items():
                if v is False:
                    context_dict['bool'][ta] = False
    print(context_dict)
    
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

    def done(self, form_list, form_dict, **kwargs):
        """This function outputs the parameters for the final page done.html

        Arguments:
            form_list {list} -- list of all the forms
            form_dict {dictionary} -- list of user submitted values for each form

        Returns:
            [html] -- Renders done.html with the context that will display the
        """
        context_dict = {}
        trade_agreements = {ta:{} for ta in agreements}

        for form in form_list:
            for k, v in form.cleaned_data.items():
                context_dict[k] = v
                for k2 in trade_agreements.keys():
                    trade_agreements[k2][k] = True
        context_dict['ta'] = trade_agreements

        context_dict = value_threshold_rule(context_dict, 'estimated_value', 'type')
        context_dict = entities_rule(context_dict, 'entities')
        context_dict = code_rule(context_dict, 'code', 'type', 'entities')
        context_dict = exceptions_rule(context_dict, 'exceptions', GeneralException)
        context_dict = exceptions_rule(context_dict, 'cfta_exceptions', CftaException)

        context_dict['bool'] = {}
        for ta in trade_agreements:
            context_dict['bool'][ta] = True
            for k, v in context_dict['ta'][ta].items():
                 if v is False:
                     context_dict['bool'][ta] = False
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
        type = Code.objects.\
            exclude(type__isnull=True).\
            exclude(type__exact='').\
            order_by('type').\
            values_list('type').\
            distinct()
        type = [i[0] for i in list(type)]
        data = {
            "type": type,
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
        code = Code.objects.\
            filter(type = type).\
            exclude(code__isnull=True).\
            exclude(code__exact='').\
            values_list('code').\
            distinct()
        code = [i[0] for i in list(code)]
        data = {
            "code": code,
        }
        return JsonResponse(data, status = 200)

