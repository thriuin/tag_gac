from guide.forms import RequiredFieldsForm, GeneralExceptionForm, LimitedTenderingForm, CftaExceptionForm
import guide.models as models
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

FORMS = [("0", RequiredFieldsForm),
         ("1", GeneralExceptionForm),
         ("2", CftaExceptionForm),
         ("3", LimitedTenderingForm)]

TEMPLATES = {"0": "mandatory_elements.html",
             "1": "exceptions.html",
             "2": "cfta_exceptions.html",
             "3": "limited_tendering.html"}

AGREEMENTS = [
    'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 
    'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta'
]


url_name='guide:form_step'
done_step_name='guide:done_step'

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def build_context_dict():
    cxt = {}
    cxt['ta'] = {ta:{} for ta in AGREEMENTS}
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
        cxt[ta][name] = False
    return cxt
    
def determine_final_coverage(agreement):
    cxt = {}
    for k1, v1 in agreement.items():
        cxt[k1] = True
        for v2 in v1.values():
            if v2 == False:
                cxt[k1] = v2
    return cxt

def organization_rule(agreement, data):
    """Checks which trade agreements apply to the selected entity

    Arguments:
        context {dictionary} -- The context keeps track of all the values submitted and the analysis
        org_name {string} -- From context this gets the submitted value

    Raises:
        ValueError: Returns value error if there is a problem with context

    Returns:
        [dictionary] -- Returns updated context dict with analysis (true or false)
    """
    model = models.Organization
    org = data['entities']

    try:
        data = model.objects.filter(name=org)
        for k in agreement.keys():
            check = data.values_list(k).get()[0]
            if check is False:
                agreement[k]['entities'] = False
            else:
                agreement[k]['entities'] = True
    except:
        raise ValueError
    return agreement


def value_threshold_rule(agreement, data):
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
    model = models.ValueThreshold
    value = int(data['estimated_value'])
    type = data['type']
    try:
        for k in agreement.keys():
            check = model.objects.filter(type=type).values_list(k).get()[0]
            if value < check:
                agreement[k]['estimated_value'] = False
            else:
                agreement[k]['estimated_value'] = True
    except:
        raise ValueError
    return agreement

def code_rule(agreement, data):
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
    code = data['code']
    commodity = data['type']
    org = data['entities']
    data = models.Code.objects.filter(code=code)

    if models.OrgTypeRule.objects.filter(org_fk=org).exists():
        goods_rule = models.OrgTypeRule.objects.filter(org_fk=org).values_list('goods').get()[0]
        tc_rule = models.OrgTypeRule.objects.filter(org_fk=org).values_list('construction').get()[0]
        if str(commodity) == 'Goods' and goods_rule:
            for k in agreement.keys():
                check = data.values_list(k).get()[0]
                agreement[k]['code'] = check
            return agreement
        if str(commodity) == 'Construction' and tc_rule:
            for k in agreement.keys():
                check = models.OrgTypeRule.objects.filter(org_fk=org).values_list(k).get()[0]
                if check is True:
                    agreement[k]['code'] = False
                elif check is False:
                    agreement[k]['code'] = True
            return agreement

    if models.CodeOrganizationExclusion.objects.filter(org_fk=org).filter(code_fk=code).exists():
        for k in agreement.keys():
            check = data.values_list(k).get()[0]
            if check is True:
                agreement[k]['code'] = False
            elif check is False:
                agreement[k]['code'] = True
        return agreement

    if str(commodity) == 'Goods':
        for k in agreement.keys():
            agreement[k]['code'] = True
    else:
        for k in agreement.keys():
            check = data.values_list(k).get()[0]
            agreement[k]['code'] = check

    return agreement



  

def exceptions_rule(agreement, data, exception_name, model):
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

    exception = data[exception_name]
    if exception == ['None']:
        for k in agreement.keys():
            agreement[k][exception_name] = True
    else:
        try:
            for k in agreement.keys():
                for ex in exception:
                    check = model.objects.filter(name=ex).values_list(k).get()[0]
                    agreement[k][exception_name] = check
                    if (agreement[k][exception_name] is False):
                        pass
                    elif (agreement[k][exception_name] is True) and (check is False):
                        pass
                    elif (agreement[k][exception_name] is True) and (check is True):
                        agreement[k][exception_name] = False
        except:
            raise ValueError
    return agreement

