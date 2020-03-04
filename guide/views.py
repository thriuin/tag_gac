from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from api.serializers import CodeSerializer
from api.models import Code, Instructions
from guide.forms import GuideFormEN, GuideFormFR



def CodeViewEN(request):
    # put try
    context_dict = {'instructions': Instructions.objects.get(id=1)}
    if request.method == "POST":
        context_dict['form'] = GuideFormEN()
    else:
        context_dict['form'] = GuideFormEN()
    return render(request, "guide.html", context_dict)


def CodeViewFR(request):
    context_dict = {'instructions': Instructions.objects.get(id=1)}
    if request.method == "POST":
        context_dict['form'] = GuideFormFR()
    else:
        context_dict['form'] = GuideFormFR()
    return render(request, "guide.html", context_dict)


class CodeListView(ListAPIView):
    serializer_class = CodeSerializer



    def get_queryset(self):
        # filter the queryset based on the filters applied
        queryList = Code.objects.all()
        type = self.request.query_params.get('type', None)
        code_system = self.request.query_params.get('code_system', None)
        code = self.request.query_params.get('code', None)

        if type:
            queryList = queryList.filter(type = type)
        if code_system:
            queryList = queryList.filter(code_system = code_system)
        if code:
            queryList = queryList.filter(code = code)


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


# def set_agreement_values(trade_agreements, record):
#     trade_agreements['nafta_annex']['setting'] = record.nafta_annex
#     trade_agreements['ccfta']['setting'] = record.ccfta
#     trade_agreements['ccofta']['setting'] = record.ccofta
#     trade_agreements['chfta']['setting'] = record.chfta
#     trade_agreements['cpafta']['setting'] = record.cpafta
#     trade_agreements['cpfta']['setting'] = record.cpfta
#     trade_agreements['ckfta']['setting'] = record.ckfta
#     trade_agreements['cufta']['setting'] = record.cufta
#     trade_agreements['wto_agp']['setting'] = record.wto_agp
#     trade_agreements['ceta']['setting'] = record.ceta
#     trade_agreements['cptpp']['setting'] = record.cptpp
#     trade_agreements['cfta']['setting'] = record.cfta
#     return trade_agreements
#
#
# def find_exemptions(form, commodity_type: str):
#     agreements = {
#         'nafta_annex_yn': False,
#         'ccfta_yn': False,
#         'ccofta_yn': False,
#         'chfta_yn': False,
#         'cpafta_yn': False,
#         'cpfta_yn': False,
#         'ckfta_yn': False,
#         'cufta_yn': False,
#         'wto_agp_yn': False,
#         'ceta_yn': False,
#         'cptpp_yn': False,
#         'cfta_yn': False,
#     }
#     reasons = {
#         'nafta_annex': [],
#         'ccfta': [],
#         'ccofta': [],
#         'chfta': [],
#         'cpafta': [],
#         'cpfta': [],
#         'ckfta': [],
#         'cufta': [],
#         'wto_agp': [],
#         'ceta': [],
#         'cptpp': [],
#         'cfta': [],
#     }
#     trade_agreements = {
#         'nafta_annex': {'setting': None, 'label': 'NAFTA', 'agreement': 'nafta_annex_yn'},
#         'ccfta': {'setting': None, 'label': 'Chile (CCFTA) ', 'agreement': 'ccfta_yn'},
#         'ccofta': {'setting': None, 'label': 'Colombia (CCoFTA)', 'agreement': 'ccofta_yn'},
#         'chfta': {'setting': None, 'label': 'Honduras (CHFTA)', 'agreement': 'chfta_yn'},
#         'cpafta': {'setting': None, 'label': 'Panama (CPaFTA)', 'agreement': 'cpafta_yn'},
#         'cpfta': {'setting': None, 'label': 'Peru (CPFTA)', 'agreement': 'cpfta_yn'},
#         'ckfta': {'setting': None, 'label': 'Korea (CKFTA)', 'agreement': 'ckfta_yn'},
#         'cufta': {'setting': None, 'label': 'Ukraine (CUFTA)', 'agreement': 'cufta_yn'},
#         'wto_agp': {'setting': None, 'label': 'WTO-AGP Canada', 'agreement': 'wto_agp_yn'},
#         'ceta': {'setting': None, 'label': 'CETA Annex 19-5', 'agreement': 'ceta_yn'},
#         'cptpp': {'setting': None, 'label': 'CPTPP Chapter 15', 'agreement': 'cptpp_yn'},
#         'cfta': {'setting': None, 'label': 'CFTA Chapter 5', 'agreement': 'cfta_yn'}
#     }
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
