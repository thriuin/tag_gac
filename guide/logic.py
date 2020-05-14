from guide.forms import RequiredFieldsFormEN, GeneralExceptionFormEN, LimitedTenderingFormEN, CftaExceptionFormEN
from guide.models import Code, ValueThreshold, Organization, GeneralException, TenderingReason, CftaException

FORMS = [("0", RequiredFieldsFormEN),
         ("1", GeneralExceptionFormEN),
         ("2", CftaExceptionFormEN),
         ("3", LimitedTenderingFormEN)]

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

def build_context_dict():
    cxt = {}
    cxt['ta'] = {ta:{} for ta in agreements}
    return cxt
        
def process_form(context, form_data):
    for k, v in form_data.items():
        context[k] = v
        for k2 in context['ta'].keys():
            context['ta'][k2][k] = True
    return context

def check_if_trade_agreement_applies(context, data, name):
    for ta in context['ta']:
        check = data.values_list(ta).get()[0]
        if check is False:
            context['ta'][ta][name] = False
        else:
            context['ta'][ta][name] = True
    return context
    
def determine_final_coverage(cxt):
    cxt['bool'] = {}
    trade_agreements = {ta:{} for ta in agreements}
    for ta in trade_agreements:
        cxt['bool'][ta] = True
        for k, v in cxt['ta'][ta].items():
            if v is False:
                cxt['bool'][ta] = False
    return cxt

def organization_rule(context, org_name):
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
    try:
        data = Organization.objects.filter(name=org)
        context = check_if_trade_agreement_applies(context, data, org_name)
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
    try:
        for ta in context['ta']:
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

    try:
        defence_rule = Organization.objects.filter(name=org).values_list('goods_rule').get()[0]
        tc_rule = Organization.objects.filter(name=org).values_list('tc').get()[0]
        if type == 'Goods' and defence_rule is False:
            for ta in context['ta']:
                context['ta'][ta][code_name] = True
            return context
        if type == 'Construction' and tc_rule is True:
            for ta in context['ta']:
                context['ta'][ta][code_name] = False
            return context
        data = Code.objects.filter(code=value)
        context = check_if_trade_agreement_applies(context, data, code_name)
        return context
    except:
        raise ValueError       

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
    if context[exception_name]:
        value = context[exception_name]
        try:
            for ta in context['ta']:
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

