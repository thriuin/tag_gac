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
from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from api.views import EntitiesView, ValueThresholdView, CommodityCodeSystemView, \
    CodeListView, TenderingReasonView, TAExceptionView, CftaExceptionView
from guide.views import MainFormView

router = routers.DefaultRouter()
router.register(r'entities', EntitiesView)
router.register(r'value_threshold', ValueThresholdView)
router.register(r'commodity_code_system', CommodityCodeSystemView)
router.register(r'code_list', CodeListView)
router.register(r'tendering_reason', TenderingReasonView)
router.register(r'ta_exception', TAExceptionView)
router.register(r'cfta_exception', CftaExceptionView)


urlpatterns = [
    path(r'tag/api/', include((router.urls, 'app_name'), namespace='instance_name')),
    path(r'tag/admin/doc/', include('django.contrib.admindocs.urls')),
    path(r'tag/admin/', admin.site.urls),
    path(r'tag/main_form/', MainFormView.as_view(), name='main_form_view')
]

