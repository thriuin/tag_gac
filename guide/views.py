from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from guide.models import Code, Instructions, ValueThreshold, Entities
from guide.forms import GuideFormEN, GuideFormFR
from django.views.generic import View


def find_exemptions(form):
    agreements = {
        'nafta_annex_yn': False,
        'ccfta_yn': False,
        'ccofta_yn': False,
        'chfta_yn': False,
        'cpafta_yn': False,
        'cpfta_yn': False,
        'ckfta_yn': False,
        'cufta_yn': False,
        'wto_agp_yn': False,
        'ceta_yn': False,
        'cptpp_yn': False,
        'cfta_yn': False,
    }

    reasons = {
        'nafta_annex': [],
        'ccfta': [],
        'ccofta': [],
        'chfta': [],
        'cpafta': [],
        'cpfta': [],
        'ckfta': [],
        'cufta': [],
        'wto_agp': [],
        'ceta': [],
        'cptpp': [],
        'cfta': [],
    }



class CodeViewEN(View):

    def get(self, request, *args, **kwargs):
        context_dict = {}
        try:
            context_dict = {'instructions': Instructions.objects.get(id=1)}
        except:
            context_dict = {'instructions': 'No Instructions'}
        context_dict['form'] = GuideFormEN()
        context_dict['show_eval']  = False
        return render(request, "guide.html", context_dict)



    def post(self, request, *args, **kwargs):
        form = GuideFormEN(request.POST)

#         check if valid
        context_dict = {}
        context_dict['form'] = form
        context_dict['show_eval'] = True
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
