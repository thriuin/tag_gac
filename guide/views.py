from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from guide.models import Code, Instructions, ValueThreshold, Entities, TAException, TenderingReason, CftaException
from guide.forms import GuideFormEN, GuideFormFR
from django.views.generic import View



def entities_rule(ent_dict, data, ent_reason):               
    try:
        for agreement in ent_dict:
            check = Entities.objects.filter(name=data).values_list(agreement).get()[0]
            if check is False:
                ent_dict[agreement]['entities'] = check
                ent_reason[agreement]['entities'] = f'Not covered by trade agreement'
            else:
                pass
    except:
        raise ValueError
    return ent_dict, ent_reason

def value_threshold_rule(val_dict, data, type, val_reason):
    try:
        for agreement in val_dict:
            check = ValueThreshold.objects.filter(type_value=type).values_list(agreement).get()[0]
            if data < check:
                val_dict[agreement]['estimated_value'] = False
                val_reason[agreement]['estimated_value'] = f'not covered'
            else:
                val_dict[agreement]['estimated_value'] = True
                val_reason[agreement]['estimated_value'] = f'covered'

    except:
        raise ValueError
    return val_dict, val_reason

def code_rule(code_dict, data, entities, type, code_reason):
    try:
        for agreement in code_dict:
            check = Code.objects.filter(code=data).values_list(agreement).get()[0]
            if check is False:
                code_dict[agreement]['code'] = False
                code_reason[agreement]['code'] = f'not covered'
            else:
                code_dict[agreement]['code'] = True
                code_reason[agreement]['code'] = f'covered'

            if type == 'Goods':
                defence_rule = Entities.objects.filter(name=entities).values_list('weapons_rule').get()[0]
                if defence_rule is True:
                    code_dict[agreement]['code'] = False
                    code_reason[agreement]['code'] = f'not covered'
                else:
                    pass
            elif type == 'Construction':
                tc_rule = Entities.objects.filter(name=entities).values_list('tc').get()[0]
                if tc_rule is True:
                    code_dict[agreement]['code'] = False
                    code_reason[agreement]['code'] = f'not covered'
                else:
                    pass
            else:
                pass
    except:
        raise ValueError
    return code_dict, code_reason

def exceptions_rule(ex_dict, exceptions, ex_reason):
    try:
        for agreement in ex_dict:
            for x in exceptions:
                    check = TAException.objects.filter(name=x).values_list(agreement).get()[0]
                    # This is a pass because if one value is true then we want to keep it true even if others are false
                    if (ex_dict[agreement]['exceptions'] is True) and (check is True):
                        ex_reason[agreement]['exceptions'] = f'exceptions apply'
                    elif (ex_dict[agreement]['exceptions'] is True) and (check is False):
                        pass
                    elif (ex_dict[agreement]['exceptions'] is False) and (check is True):
                        ex_dict[agreement]['exceptions'] = True
                        ex_reason[agreement]['exceptions'] = f'exceptions apply'
                    elif (ex_dict[agreement]['exceptions'] is False) and (check is False):
                        ex_reason[agreement]['exceptions'] = f'no exceptions apply'

    except:
        raise ValueError
    return ex_dict, ex_reason

def limited_tendering_reasons_func(lim_dict, limited_tendering_reason, lim_reason):
    try:
        for agreement in lim_dict:
            for x in limited_tendering_reason:
                check = TenderingReason.objects.filter(name=x).values_list(agreement).get()[0]
                if (lim_dict[agreement]['limited_tendering'] is True) and (check is True):
                    lim_reason[agreement]['limited_tendering'] = f'exceptions apply'
                elif (lim_dict[agreement]['limited_tendering'] is True) and (check is False):
                    pass
                elif (lim_dict[agreement]['limited_tendering'] is False) and (check is True):
                    lim_reason[agreement]['limited_tendering'] = f'exceptions apply'
                elif (lim_dict[agreement]['limited_tendering'] is False) and (check is False):
                    lim_reason[agreement]['limited_tendering'] = f'no exceptions apply'
    except:
        raise ValueError
    return lim_dict, lim_reason


def cfta_exceptions_func(cfta_dict, cfta_exceptions, cfta_reason):
    try:
        for agreement in cfta_dict:
            for x in cfta_exceptions:
                check = CftaException.objects.filter(name=x).values_list(agreement).get()[0]
                if (cfta_dict[agreement]['cfta_exceptions'] is True) and (check is True):
                    cfta_reason[agreement]['cfta_exceptions'] = f'exceptions apply'
                elif (cfta_dict[agreement]['cfta_exceptions'] is True) and (check is False):
                    pass
                elif (cfta_dict[agreement]['cfta_exceptions'] is False) and (check is True):
                    cfta_reason[agreement]['cfta_exceptions'] = f'exceptions apply'
                elif (cfta_dict[agreement]['cfta_exceptions'] is False) and (check is False):
                    cfta_reason[agreement]['limited_tendering'] = f'no exceptions apply'
    except:
        raise ValueError
    return cfta_dict, cfta_reason


class CodeViewEN(View):

    def get(self, request, *args, **kwargs):
        context_dict = {}
        try:
            context_dict = {'instructions': Instructions.objects.get(id=1)}
        except:
            context_dict = {'instructions': 'No Instructions'}
        form = GuideFormEN()
        context_dict['form'] = form
        context_dict['show_eval']  = False
        return render(request, "guide.html", context_dict)

    def post(self, request, *args, **kwargs):
        form = GuideFormEN(request.POST)

        if form.is_valid():
            print('hello from valid')
        else:
            print('form not valid')
            print(form.errors)
        
        rules = {
            'entities': True,
            'estimated_value': True,
            'type': True,
            'code_system': True,
            'code': True,
            'exceptions': False,
            'limited_tendering': False,
            'cfta_exceptions': False
        }
        
        reason = {
            'entities': {},
            'estimated_value': {},
            'type': {},
            'code_system': {},
            'code': {},
            'exceptions': {},
            'limited_tendering': {},
            'cfta_exceptions': {}
        }
        trade_agreements = ['nafta_annex', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']
        
        agreements = {}
        reasons = {}
        for ta in trade_agreements:
            agreements[ta] = {}
            reasons[ta] = {}
            for key, value in rules.items():
                agreements[ta][key] = value
            for key, value in reason.items():
                reasons[ta][key] = value
        
        ta = agreements

        context_dict = {}
        for key in reason.keys():
            if form.cleaned_data is not None:
                context_dict[key] = form.cleaned_data[key]
            else:
                context_dict[key] = None
                print(key)
            print(context_dict[key])

        ta, reasons = entities_rule(ta, context_dict['entities'], reasons)
        ta, reasons = value_threshold_rule(ta, context_dict['estimated_value'], context_dict['type'], reasons)
        ta, reasons = code_rule(ta, context_dict['code'], context_dict['entities'], context_dict['type'], reasons)

        if context_dict['exceptions']:
            ta, reasons = exceptions_rule(ta, context_dict['exceptions'], reasons)
        else:
            context_dict['exceptions'] = ['None']


        if context_dict['limited_tendering']:
            ta, reasons = limited_tendering_reasons_func(ta, context_dict['limited_tendering'], reasons)
        else:
            context_dict['limited_tendering'] = ['None']

        if context_dict['cfta_exceptions']:
            ta, reasons = cfta_exceptions_func(ta, context_dict['cfta_exceptions'], reasons)
        else:
            context_dict['cfta_exceptions'] = ['None']

        context_dict['rules'] = ta
        context_dict['reasons'] = reasons
        context_dict['show_eval'] = True
        print(context_dict['cfta_exceptions'])

        return render (request, "guide.html", context_dict)



class CodeViewFR(View):

    def get(self, request, *args, **kwargs):
        try:
            context_dict = {'instructions': Instructions.objects.get(id=1)}
        except:
            context_dict = {'instructions': 'No instructions'}

        if request.method == "POST":
            context_dict['form'] = GuideFormFR()
        else:
            context_dict['form'] = GuideFormFR()
        return render(request, "guide.html", context_dict)



def getType(request):
    # get all the types from the database
    # null and blank values
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



def getCodeSystem(request):
    # get the code systems from the database
    # database excluding null and blank values
    if request.method == "GET" and request.is_ajax():
        type = request.GET.get('type')
        code_system = Code.objects.\
            filter(type = type).\
            exclude(code_system__isnull=True).\
            exclude(code_system__exact='').\
            order_by('code_system').\
            values_list('code_system').\
            distinct()
        code_system = [i[0] for i in list(code_system)]
        data = {
            "code_system": code_system,
        }
        return JsonResponse(data, status = 200)



def getCode(request):
    # get the type and code systems and filter to get code
    # database excluding null and blank values
    if request.method == "GET" and request.is_ajax():
        code_system = request.GET.get('code_system')
        type = request.GET.get('type')
        code = Code.objects.\
            filter(type = type).\
            filter(code_system = code_system).\
            exclude(code__isnull=True).\
            exclude(code__exact='').\
            values_list('code').\
            distinct()
        code = [i[0] for i in list(code)]
        data = {
            "code": code,
        }
        return JsonResponse(data, status = 200)




#     desc_en = ""
#     dollars = form.cleaned_data['estimated_value']
#     if commodity_type == 'goods':
#         if 'goods_codes' in form.cleaned_data and form.cleaned_data['goods_codes'] is not None:
#             goods = GoodsFscCode.objects.get(id=form.cleaned_data['goods_codes'].id)
#             set_agreement_values(trade_agreements, goods)
#             desc_en = goods.fs_code_desc
#
#     elif commodity_type == 'services':
#         if 'services_code' in form.cleaned_data and form.cleaned_data['services_codes'] is not None:
#             services = ServicesCcsCode.objects.get(id=form.cleaned_data['services_codes'].id)
#             set_agreement_values(trade_agreements, services)
#             desc_en = services.ccs_level_2
#
#     elif commodity_type == 'construction':
#         if 'construction_code' in form.cleaned_data and form.cleaned_data['construction_code'] is not None:
#             construction = ConstructionCcsCode.objects.get(id=form.cleaned_data['construction_code'].id)
#             set_agreement_values(trade_agreements, construction)
#             desc_en = construction.fs_code_desc
#
#     # Find the exemptions based on commodity type
#     for ta in trade_agreements:
#         if trade_agreements[ta]['setting']:
#             agreements[trade_agreements[ta]['agreement']] = True
#             reasons[ta].append('{0} are exempt under {1}'.format(desc_en, trade_agreements[ta]['label']))
#
#     # Find the exemptions based on dollar value
#     vt = ValueThreshold.objects.get(desc_en=commodity_type)
#     set_agreement_values(trade_agreements, vt)
#     for ta in trade_agreements:
#         if trade_agreements[ta]['setting'] is not None and dollars < trade_agreements[ta]['setting']:
#             agreements[trade_agreements[ta]['agreement']] = True
#             reasons[ta].append('{0} under {1} are exempt under {2}'.format(commodity_type, trade_agreements[ta]['setting'],
#                                                                            trade_agreements[ta]['label']))
#
#     return agreements, reasons
#
# class GuideListView(ListView):
#     model = ModelGuide
#     context_object_name = 'guide'
#
#
# class GuideCreateView(CreateView):
#     model = ModelGuide
#     fields = (
#         'estimated_value',
#         'federal_entities',
#         'commodity_type',
#         'commodity_code',
#         'exceptions',
#         'limited_tendering',
#         'cfta_ex'
#     )
#     success_url = reverse_lazy('guide_list')
#
#
# class GuideUpdateView(UpdateView):
#     model = ModelGuide
#     fields = (
#         'estimated_value',
#         'federal_entities',
#         'commodity_type',
#         'commodity_code',
#         'exceptions',
#         'limited_tendering',
#         'cfta_ex'
#     )
#     success_url = reverse_lazy('guide_list')

# class GuideListView(View):
#     def __init__(self):
#         super().__init__()
#
#     def get(self, request, *args, **kwargs):
#         form = GuideFormEN()
#         # do not display the evaluation section of the form
#         return render(request, 'guide_form.html', {'form': form, 'show_eval': False})
#
#     def post(self, request, *args, **kwargs):
#         # create a form instance and populate it with data from the request:
#         form = GuideFormEN(request.POST)
#         context = {'show_eval': False}
#         # check whether it's valid:
#         if form.is_valid():
#             commodity_type = ''
#             if 'commodity_type' in form.cleaned_data and form.cleaned_data['commodity_type'] is not None:
#                 commodity_type = form.cleaned_data['commodity_type']
#             elif 'commodity_type' in form.data and form.data['commodity_type'] in ('goods', 'services', 'construction'):
#                 commodity_type = form.data['commodity_type']
#             if commodity_type != '':
#                 ta = find_exemptions(form, commodity_type)
#                 # forward a merged dictionary of exemptions and  reasons to the form for display
#                 context = {**ta[0], **ta[1]}
#                 # show the evaluation section on the page
#                 context['show_eval'] = True
#         context['form'] = form
#         return render(request, 'guide_form.html', context)
