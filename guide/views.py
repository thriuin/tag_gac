from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import View
from rest_framework import viewsets
from guide.forms import GuideForm
from guide.models import GoodsCode, ConstructionCode, ServicesCode, TenderingReason, ValueThreshold
from guide.serializers import GoodsSerializer, ConstructionSerializer, ServicesSerializer, TenderingSerializer


class GoodsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Goods Procurement Codes to be viewed or edited.
    """
    queryset = GoodsCode.objects.all().order_by('fs_code_desc')
    serializer_class = GoodsSerializer


class ConstructionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Construction Procurement Codes  to be viewed or edited.
    """
    queryset = ConstructionCode.objects.all().order_by('fs_code_desc')
    serializer_class = ConstructionSerializer


class ServicesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Services Procurement Codes  to be viewed or edited.
    """
    queryset = ServicesCode.objects.all().order_by('ccs_level_2')
    serializer_class = ServicesSerializer


class TenderingReasonsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tendering Reasons to be viewed or edited.
    """
    queryset = TenderingReason.objects.all().order_by('desc_en')
    serializer_class = TenderingSerializer


class GuideView(View):

    def __init__(self):
        super().__init__()

    def get(self, request):
        context = dict()
        
        return render(request, "guide.html", context)


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
    }
    dollars = form.cleaned_data['estimated_value']
    if 'goods_codes' in form.cleaned_data and form.cleaned_data['goods_codes'] is not None:
        goods = GoodsCode.objects.get(id=form.cleaned_data['goods_codes'].id)
    else:
        goods = None
    if 'services_code' in form.cleaned_data and form.cleaned_data['services_codes'] is not None:
        services = ServicesCode.objects.get(id=form.cleaned_data['services_codes'].id)
    else:
        services = None
    if 'construction_code' in form.cleaned_data and form.cleaned_data['construction_code'] is not None:
        construction = ConstructionCode.objects.get(id=form.cleaned_data['construction_code'].id)
    else:
        construction = None
    commodity_type = ''
    if 'commodity_type' in form.cleaned_data and form.cleaned_data['commodity_type'] is not None:
        commodity_type = form.cleaned_data['commodity_type']
    elif 'commodity_type' in form.data and form.data['commodity_type'] in ('goods', 'services', 'construction'):
        commodity_type = form.data['commodity_type']
    if commodity_type != '':
        vt = ValueThreshold.objects.get(desc_en=commodity_type)

        if dollars < vt.nafta_annex:
            agreements['nafta_annex_yn'] = True
            reasons['nafta_annex'].append('Commodities under {0} are exempt under NAFTA Annex'.format(vt.nafta_annex))
        if dollars < vt.ccfta:
            agreements['ccfta_yn'] = True
            reasons['ccfta'].append('Commodities under {0} are exempt under CCFTA'.format(vt.ccfta))
        if dollars < vt.ccofta:
            agreements['ccofta_yn'] = True
            reasons['ccofta'].append('Commodities under {0} are exempt under CCoFTA'.format(vt.ccofta))
            # @todo pick it up here

        if commodity_type == 'goods' and goods is not None:
            if goods.nafta_annex:
                agreements['nafta_annex_yn'] = True
                reasons['nafta_annex'].append(
                    '{0} are exempt under NAFTA Annex'.format(goods.fs_code_desc))
            if goods.ccfta:
                agreements['ccfta_yn'] = True
                reasons['ccfta'].append(
                    '"{0}" are exempt under CCFTA'.format(goods.fs_code_desc))

    return agreements, reasons


class GuideFormView(View):
    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        form = GuideForm()
        return render(request, 'guide_form.html', {'form': form, 'show_eval': False})

    def post(self, request, *args, **kwargs):
        # create a form instance and populate it with data from the request:
        form = GuideForm(request.POST)
        context = {'show_eval': False}
        # check whether it's valid:
        if form.is_valid():
            ta = find_exemptions(form)
            context = {**ta[0], **ta[1]}
            context['show_eval'] = True
            print('Valid')
        context['form'] = form
        return render(request, 'guide_form.html', context)


class EvaluateResults(View):

    def __init__(self):
        super().__init__()

    def get(self, request: HttpRequest):
        if request.method == 'POST':
            post_data = request.POST
            print(post_data)

