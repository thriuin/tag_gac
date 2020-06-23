from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from guide.views import ajax_type, ajax_code, TradeForm, lt_condition, EntitiesAutocomplete
from django.shortcuts import redirect
from guide.logic import FORMS, url_name, done_step_name

trade_wizard = TradeForm.as_view(
    FORMS, 
    condition_dict={"3": lt_condition}, 
    url_name=url_name, 
    done_step_name=done_step_name
)

urlpatterns = [
    path('<step>/', trade_wizard, name='form_step'),
    path('done/', trade_wizard, name='done_step'),
    path('', lambda request: redirect('0/', permanent=True)),
    url('^.*$', lambda request: redirect('0/', permanent=True))
]
