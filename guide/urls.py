from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from guide.views import *


urlpatterns = [
    path('', Guide),
    path("wine_listing/", GuideListing.as_view(), name ='listing'),
    path("ajax/countries/", getType, name ='get_type'),
    path("ajax/getCodeSystem/", getCodeSystem, name='get_code_system'),
    path("ajax/province/", getCodeList, name = 'get_code_list')
]