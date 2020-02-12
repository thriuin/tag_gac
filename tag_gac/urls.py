"""tag_gac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from guide.views import GuideView, CommodityTypeViewSet, \
    GoodsFscViewSet, GoodsUnspscViewSet, \
    ServicesCcsViewSet, ServicesCpcViewSet, ServicesUnspscViewSet, \
    ConstructionCcsViewSet, ConstructionCpcViewSet, ConstructionUnspscViewset, \
    TenderingReasonsViewSet, TAExceptionsViewSet, CftaExceptionsViewSet, \
    FederalEntitiesViewSet, GuideListView, GuideCreateView, GuideUpdateView


urlpatterns = [
    path('tag/admin/', admin.site.urls),
    path('tag/', GuideListView.as_view(), name='guide_list'),
    path('tag/add/', GuideCreateView.as_view(), name='guide_create'),
    path('tag/commodity/', GuideUpdateView.as_view(), name='guide_update'),
    path('tag/commoditytype', CommodityTypeViewSet.as_view({'get': 'list'}), name='commodity_type_create_view'),
    path('tag/guide/', GuideView.as_view(), name='Guide'),  # Temporary demo of SurveyJS
    path('tag/goodsfsc/', GoodsFscViewSet.as_view({'get': 'list'})),
    path('tag/goodsunspsc/', GoodsUnspscViewSet.as_view({'get': 'list'})),
    path('tag/constructionccs/', ConstructionCcsViewSet.as_view({'get': 'list'})),
    path('tag/constructioncpc/', ConstructionCpcViewSet.as_view({'get': 'list'})),
    path('tag/constructionunspsc/', ConstructionUnspscViewset.as_view({'get': 'list'})),
    path('tag/servicesccs/', ServicesCcsViewSet.as_view({'get': 'list'})),
    path('tag/servicescpc/', ServicesCpcViewSet.as_view({'get': 'list'})),
    path('tag/servicesunspsc/', ServicesUnspscViewSet.as_view({'get': 'list'})),
    path('tag/tendering_reasons/', TenderingReasonsViewSet.as_view({'get': 'list'})),
    path('tag/taexceptions/', TAExceptionsViewSet.as_view({'get': 'list'})),
    path('tag/cftaexceptions/', CftaExceptionsViewSet.as_view({'get': 'list'})),
    path('tag/federalentities/', FederalEntitiesViewSet.as_view({'get': 'list'})),
    path('tag/evaluate/', GuideListView.as_view(), name='EvaluateForm')
]
