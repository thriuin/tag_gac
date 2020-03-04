from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from guide.views import CodeViewEN, CodeViewFR, CodeListView, getType, getCodeSystem, getCode

urlpatterns = [
    path('en/', CodeViewEN),
    path('fr/', CodeViewFR),
    path("code_list/", CodeListView.as_view(), name ='listing'),
    path("ajax/type/", getType, name = 'get_type'),
    path("ajax/code_system/", getCodeSystem, name = 'get_code_system'),
	path("ajax/code/", getCode, name = 'get_code')
]