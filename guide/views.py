from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import View
from rest_framework import viewsets
from guide.forms import GuideForm
from guide.models import GoodsOGDCode, GoodsMilitaryCode, ConstructionCode, ServicesCode, TenderingReason, ValueThreshold, FederalEntities
from guide.serializers import GoodsOGDSerializer, GoodsMilitarySerializer, ConstructionSerializer, ServicesSerializer, TenderingSerializer, FederalEntitiesSerializer


class GoodsOGDViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Goods Procurement Codes to be viewed or edited.
    """
    queryset = GoodsOGDCode.objects.all().order_by('fs_code_desc')
    serializer_class = GoodsOGDSerializer


class GoodsMilitaryViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows the military goods procurement codes to be viewed or edited.
    '''
    queryset = GoodsMilitaryCode.objects.all().order_by('fs_code_desc')
    serializer_class = GoodsMilitarySerializer


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


class FederalEntitiesViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows Federal Entities to be viewed and edited
    '''
    queryset = FederalEntities.objects.all().order_by('name_en')
    serializer_class = FederalEntitiesSerializer


class GuideView(View):

    def __init__(self):
        super().__init__()

    def get(self, request):
        context = dict()
        
        return render(request, "guide.html", context)


def set_agreement_values(trade_agreements, record):
    trade_agreements['nafta_annex']['setting'] = record.nafta_annex
    trade_agreements['ccfta']['setting'] = record.ccfta
    trade_agreements['ccofta']['setting'] = record.ccofta
    trade_agreements['chfta']['setting'] = record.chfta
    trade_agreements['cpafta']['setting'] = record.cpafta
    trade_agreements['cpfta']['setting'] = record.cpfta
    trade_agreements['ckfta']['setting'] = record.ckfta
    trade_agreements['cufta']['setting'] = record.cufta
    trade_agreements['wto_agp']['setting'] = record.wto_agp
    trade_agreements['ceta']['setting'] = record.ceta
    trade_agreements['cptpp']['setting'] = record.cptpp
    trade_agreements['cfta']['setting'] = record.cfta
    return trade_agreements


def find_exemptions(form, commodity_type: str):
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
    trade_agreements = {
        'nafta_annex': {'setting': None, 'label': 'NAFTA', 'agreement': 'nafta_annex_yn'},
        'ccfta': {'setting': None, 'label': 'Chile (CCFTA) ', 'agreement': 'ccfta_yn'},
        'ccofta': {'setting': None, 'label': 'Colombia (CCoFTA)', 'agreement': 'ccofta_yn'},
        'chfta': {'setting': None, 'label': 'Honduras (CHFTA)', 'agreement': 'chfta_yn'},
        'cpafta': {'setting': None, 'label': 'Panama (CPaFTA)', 'agreement': 'cpafta_yn'},
        'cpfta': {'setting': None, 'label': 'Peru (CPFTA)', 'agreement': 'cpfta_yn'},
        'ckfta': {'setting': None, 'label': 'Korea (CKFTA)', 'agreement': 'ckfta_yn'},
        'cufta': {'setting': None, 'label': 'Ukraine (CUFTA)', 'agreement': 'cufta_yn'},
        'wto_agp': {'setting': None, 'label': 'WTO-AGP Canada', 'agreement': 'wto_agp_yn'},
        'ceta': {'setting': None, 'label': 'CETA Annex 19-5', 'agreement': 'ceta_yn'},
        'cptpp': {'setting': None, 'label': 'CPTPP Chapter 15', 'agreement': 'cptpp_yn'},
        'cfta': {'setting': None, 'label': 'CFTA Chapter 5', 'agreement': 'cfta_yn'}
    }
    desc_en = ""
    dollars = form.cleaned_data['estimated_value']
    if commodity_type == 'goods':
        if 'goods_codes' in form.cleaned_data and form.cleaned_data['goods_codes'] is not None:
            goods = GoodsOGDCode.objects.get(id=form.cleaned_data['goods_codes'].id)
            set_agreement_values(trade_agreements, goods)
            desc_en = goods.fs_code_desc

    elif commodity_type == 'services':
        if 'services_code' in form.cleaned_data and form.cleaned_data['services_codes'] is not None:
            services = ServicesCode.objects.get(id=form.cleaned_data['services_codes'].id)
            set_agreement_values(trade_agreements, services)
            desc_en = services.ccs_level_2

    elif commodity_type == 'construction':
        if 'construction_code' in form.cleaned_data and form.cleaned_data['construction_code'] is not None:
            construction = ConstructionCode.objects.get(id=form.cleaned_data['construction_code'].id)
            set_agreement_values(trade_agreements, construction)
            desc_en = construction.fs_code_desc

    # Find the exemptions based on commodity type
    for ta in trade_agreements:
        if trade_agreements[ta]['setting']:
            agreements[trade_agreements[ta]['agreement']] = True
            reasons[ta].append('{0} are exempt under {1}'.format(desc_en, trade_agreements[ta]['label']))

    # Find the exemptions based on dollar value
    vt = ValueThreshold.objects.get(desc_en=commodity_type)
    set_agreement_values(trade_agreements, vt)
    for ta in trade_agreements:
        if trade_agreements[ta]['setting'] is not None and dollars < trade_agreements[ta]['setting']:
            agreements[trade_agreements[ta]['agreement']] = True
            reasons[ta].append('{0} under {1} are exempt under {2}'.format(commodity_type, trade_agreements[ta]['setting'],
                                                                           trade_agreements[ta]['label']))

    return agreements, reasons


class GuideFormView(View):
    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        form = GuideForm()
        # do not display the evaluation section of the form
        return render(request, 'guide_form.html', {'form': form, 'show_eval': False})

    def post(self, request, *args, **kwargs):
        # create a form instance and populate it with data from the request:
        form = GuideForm(request.POST)
        context = {'show_eval': False}
        # check whether it's valid:
        if form.is_valid():
            commodity_type = ''
            if 'commodity_type' in form.cleaned_data and form.cleaned_data['commodity_type'] is not None:
                commodity_type = form.cleaned_data['commodity_type']
            elif 'commodity_type' in form.data and form.data['commodity_type'] in ('goods', 'services', 'construction'):
                commodity_type = form.data['commodity_type']
            if commodity_type != '':
                ta = find_exemptions(form, commodity_type)
                # forward a merged dictionary of exemptions and  reasons to the form for display
                context = {**ta[0], **ta[1]}
                # show the evaluation section on the page
                context['show_eval'] = True
        context['form'] = form
        return render(request, 'guide_form.html', context)

