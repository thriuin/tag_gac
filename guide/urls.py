from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from guide.views import ajax_type, ajax_code, TradeForm, lt_condition, FORMS, url_name, done_step_name

trade_wizard = TradeForm.as_view(
    FORMS, 
    condition_dict={"3": lt_condition}, 
    url_name=url_name, 
    done_step_name=done_step_name
)

urlpatterns = [
    url(r'^en/(?P<step>.+)/$', trade_wizard, name='form_step'),
    url('/en/done/', trade_wizard, name=done_step_name),
    path("ajax/type/", ajax_type, name = 'ajax_type'),
	path("ajax/code/", ajax_code, name = 'ajax_code')
]
