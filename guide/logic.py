from guide.forms import RequiredFieldsForm, GeneralExceptionForm, LimitedTenderingForm, CftaExceptionForm
from guide.models import Code, ValueThreshold, Organization, GeneralException, LimitedTenderingReason, CftaException
# from guide.models import OrganizationWithCommodityCodeRules, OrganizationWithCommodityTypeRules
FORMS = [("0", RequiredFieldsForm),
         ("1", GeneralExceptionForm),
         ("2", CftaExceptionForm),
         ("3", LimitedTenderingForm)]

TEMPLATES = {"0": "mandatory_elements.html",
             "1": "exceptions.html",
             "2": "cfta_exceptions.html",
             "3": "limited_tendering.html"}

agreements = [
    'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 
    'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta'
]

url_name='guide:form_step'
done_step_name='done_step'

def build_context_dict():
    cxt = {}
    cxt['ta'] = {ta:{} for ta in agreements}
    return cxt
        
def process_form(cxt, form_data):
    for k, v in form_data.items():
        cxt[k] = v
        for k2 in cxt['ta'].keys():
            cxt['ta'][k2][k] = True
    return cxt

def check_if_trade_agreement_applies(ta, cxt, data, name):
    check = data.values_list(ta).get()[0]
    if check is False:
        cxt['ta'][ta][name] = False

    return cxt
    
def determine_final_coverage(cxt):
    cxt['bool'] = {}
    trade_agreements = {ta:{} for ta in agreements}
    for ta in trade_agreements:
        cxt['bool'][ta] = True
        for v in cxt['ta'][ta].values():
            if v is False:
                cxt['bool'][ta] = False
    return cxt

def organization_rule(cxt, org_name):
    """Checks which trade agreements apply to the selected entity

    Arguments:
        context {dictionary} -- The context keeps track of all the values submitted and the analysis
        org_name {string} -- From context this gets the submitted value

    Raises:
        ValueError: Returns value error if there is a problem with context

    Returns:
        [dictionary] -- Returns updated context dict with analysis (true or false)
    """
    org = cxt[org_name]
    try:
        data = Organization.objects.filter(name=org)
        for ta in cxt['ta']:
            cxt = check_if_trade_agreement_applies(ta, cxt, data, org_name)
    except:
        raise ValueError
    return cxt

def value_threshold_rule(cxt, value_name, type_name):
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
    value = cxt[value_name]
    type = cxt[type_name]
    try:
        for ta in cxt['ta']:
            check = ValueThreshold.objects.filter(type_value=type).values_list(ta).get()[0]
            if value < check:
                cxt['ta'][ta][value_name] = False
            else:
                cxt['ta'][ta][value_name] = True
    except:
        raise ValueError
    return cxt

def code_rule(cxt, code_name, type_name, org_name):
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
    value = cxt[code_name]
    type = cxt[type_name]
    org = cxt[org_name]

    if OrganizationWithCommodityTypeRules.objects.filter(org_fk_en_ca=org).exists():
        defence_rule = OrganizationWithCommodityTypeRules.objects.filter(org_fk_en_ca=org).values_list('goods_rule').get()[0]
        tc_rule = OrganizationWithCommodityTypeRules.objects.filter(org_fk_en_ca=org).values_list('tc').get()[0]
        if type == 'Goods' and defence_rule:
            data = Code.objects.filter(code=value)
            for ta in cxt['ta']:
                cxt = check_if_trade_agreement_applies(ta, cxt, data, code_name)
        if type == 'Construction' and tc_rule:
            for ta in cxt['ta']:
                if ta == 'cfta':
                    pass
                else:
                    cxt['ta'][ta][code_name] = False


    if OrganizationWithCommodityCodeRules.objects.filter(org_fk_en_ca=org).filter(code_fk_en_ca=value).exists():
        data = OrganizationWithCommodityCodeRules.objects.filter(org_fk_en_ca=org).filter(code_fk_en_ca=value)
        for ta in cxt['ta']:
            cxt = check_if_trade_agreement_applies(ta, cxt, data, code_name)

    if type == 'Goods':
        pass
    else:
        data = Code.objects.filter(code=value)
        for ta in cxt['ta']:
            cxt = check_if_trade_agreement_applies(ta, cxt, data, code_name)

    return cxt     

def exceptions_rule(cxt, exception_name, model):
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
    if cxt[exception_name]:
        value = cxt[exception_name]
        try:
            for ta in cxt['ta']:
                for ex in value:
                    check = model.objects.filter(name=ex).values_list(ta).get()[0]

                    if (cxt['ta'][ta][exception_name] is False):
                        pass
                    elif (cxt['ta'][ta][exception_name] is True) and (check is False):
                        pass
                    elif (cxt['ta'][ta][exception_name] is True) and (check is True):
                        cxt['ta'][ta][exception_name] = False
        except:
            raise ValueError
    else:
        cxt[exception_name]= ['None']
    return cxt

