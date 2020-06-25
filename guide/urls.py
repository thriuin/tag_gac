from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from guide.views import TradeForm, lt_condition, EntitiesAutocomplete, TypeAutocomplete, CodeAutocomplete
from django.shortcuts import redirect
from guide.logic import FORMS, url_name, done_step_name
from django.views.generic.base import RedirectView

trade_wizard = TradeForm.as_view(
    FORMS, 
    condition_dict={"3": lt_condition}, 
    url_name=url_name, 
    done_step_name=done_step_name
)
app_name='guide'
urlpatterns = [
    path('entities-autocomplete/', EntitiesAutocomplete.as_view(), name='entities-autocomplete'),
    path('type-autocomplete/', TypeAutocomplete.as_view(), name='type-autocomplete'),
    path('code-autocomplete/', CodeAutocomplete.as_view(), name='code-autocomplete'),
    path('markdownx/', include('markdownx.urls')),
    path('form/<step>/', trade_wizard, name='form_step'),
    path('form/done/', trade_wizard, name='done_step'),
    re_path('form/', RedirectView.as_view(url='0/')),
    re_path('', RedirectView.as_view(url='form/0/')),
    re_path(r'^.*$', RedirectView.as_view(url='form/0/')),
]