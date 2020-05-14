# from guide.forms import RequiredFieldsFormEN, GeneralExceptionFormEN, TenderingReasonFormEN, CftaExceptionFormEN
# from guide.models import Code, ValueThreshold, Organization, GeneralException, TenderingReason, CftaException

# STEP_ZERO = '0'
# STEP_ONE = '1'
# STEP_TWO = '2'
# STEP_THREE = '3'

# FORMS = [(STEP_ZERO, RequiredFieldsFormEN),
#          (STEP_ONE, GeneralExceptionFormEN),
#          (STEP_TWO, CftaExceptionFormEN),
#          (STEP_THREE, TenderingReasonFormEN)]

# TEMPLATES = {STEP_ZERO: "mandatory_elements.html",
#              STEP_ONE: "exceptions.html",
#              STEP_TWO: "cfta_exceptions.html",
#              STEP_THREE: "limited_tendering.html"}

# agreements = [
#     'nafta', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 
#     'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta'
# ]

# url_name='guide:form_step'
# done_step_name='guide:done_step'

# def entities_rule(context, org_name):
#     """Checks which trade agreements apply to the selected entity

#     Arguments:
#         context {dictionary} -- The context keeps track of all the values submitted and the analysis
#         org_name {string} -- From context this gets the submitted value

#     Raises:
#         ValueError: Returns value error if there is a problem with context

#     Returns:
#         [dictionary] -- Returns updated context dict with analysis (true or false)
#     """
#     org = context[org_name]
#     trade_agreements = context['ta']
#     try:
#         for ta in trade_agreements:
#             check = Organization.objects.filter(name=org).values_list(ta).get()[0]
#             if check is False:
#                 context['ta'][ta][org_name] = False
#             else:
#                 context['ta'][ta][org_name] = True
#     except:
#         raise ValueError
#     return context

# def value_threshold_rule(context, value_name, type_name):
#     """Checks whether the value submitted by the user is less than or greater than the
#     value in the trade agreement.

#     Arguments:
#         context {dictionary} -- The context keeps track of all the values submitted and the analysis
#         col_estimated_value {string} -- From context this gets the submitted value
#         col_type {string} -- From context this gets the submitted value

#     Raises:
#         ValueError: Output if there is an error with the context

#     Returns:
#         [dictionary] -- Updates context with the analyzed value, either true or false
#     """
#     value = context[value_name]
#     type = context[type_name]
#     trade_agreements = context['ta']
#     try:
#         for ta in trade_agreements:
#             check = ValueThreshold.objects.filter(type_value=type).values_list(ta).get()[0]
#             if value < check:
#                 context['ta'][ta][value_name] = False
#             else:
#                 context['ta'][ta][value_name] = True
#     except:
#         raise ValueError
#     return context

# def code_rule(context, code_name, type_name, org_name):
#     """Checks if the code selected by the user is covered by each trade agreement.

#     Arguments:
#         context {dictionary} -- Context tracks user input and analysis
#         col_code {string} -- String to select user value for code from the context
#         type_col {string} -- String to select user value for type from the context
#         org_name {string} -- String to select user value for org from the context

#     Raises:
#         ValueError: If error in context

#     Returns:
#         [dictionary] -- Returns context with updated analysis
#     """
#     value = context[code_name]
#     type = context[type_name]
#     org = context[org_name]
#     trade_agreements = context['ta']

#     try:
#         if type == 'Goods':
#             defence_rule = Organization.objects.filter(name=org).values_list('goods_rule').get()[0]
#             for ta in trade_agreements:
#                 if defence_rule is False:
#                     context['ta'][ta][code_name] = True
#                 else:
#                     context['ta'][ta][code_name] = False
#                 return context
#         elif type == 'Construction':
#             tc_rule = Organization.objects.filter(name=org).values_list('tc').get()[0]
#             for ta in trade_agreements:
#                 if tc_rule is False:
#                     context['ta'][ta][code_name] = True
#                 else:
#                     context['ta'][ta][code_name] = False
#             return context
#         else:
#             for ta in trade_agreements:
#                 check = Code.objects.filter(code=value).values_list(ta).get()[0]
#                 if check is False:
#                     context['ta'][ta][code_name] = False
#                 else:
#                     context['ta'][ta][code_name] = True
#     except:
#         raise ValueError
#     return context

# def exceptions_rule(context, exception_name, model):
#     """This function goes through the exceptions that the user selected and checks which trade agreements
#     apply to each exception.  If a user selects a trade agreements and an exception applies then that
#     agreement is set to False.

#     Arguments:
#         context {dictionary} -- Context tracks user input and analysis
#         col {[type]} -- From context this gets the submitted value
#         model {model} -- This gets the model related to the submitted value

#     Raises:
#         ValueError: If error in context

#     Returns:
#         Dictionary -- Returns updated context dictionary with analysis
#     """
#     trade_agreements = context['ta']
#     if context[exception_name]:
#         value = context[exception_name]
#         try:
#             for ta in trade_agreements:
#                 for ex in value:
#                     check = model.objects.filter(name=ex).values_list(ta).get()[0]

#                     if (context['ta'][ta][exception_name] is False):
#                         pass
#                     elif (context['ta'][ta][exception_name] is True) and (check is False):
#                         pass
#                     elif (context['ta'][ta][exception_name] is True) and (check is True):
#                         context['ta'][ta][exception_name] = False
#         except:
#             raise ValueError
#     else:
#         context[exception_name]= ['None']
#     return context



# def build_context_dict():
#     form_list = [f[1] for f in FORMS]
#     cxt = {
#         'ta': {},
#         'bool': {}
#         }

#     fields = {}
#     for fl in form_list:
#         for k in fl.declared_fields.keys():
#             cxt.update({k:None})
#             fields.update({k:True})

#     for k in agreements:
#         cxt['bool'][k] = True
#         cxt['ta'][k] = fields

#     return cxt


# def final_trade_coverage(context_dict):
#     trade_agreements = context_dict['ta']
#     for ta in trade_agreements:
#         context_dict['bool'][ta] = True
#         for k, v in context_dict['ta'][ta].items():
#                 if v is False:
#                     context_dict['bool'][ta] = False
#     return context_dict