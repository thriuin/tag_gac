from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from api.models import Entities, ValueThreshold, CommodityCodeSystem, \
    CodeList, TenderingReason, TAException, CftaException
from guide.forms import MainForm
from django.shortcuts import render

class MainFormView(TemplateView):
    template_name = 'main_form.html'

    def get_context_data(self, **kwargs):
        context = super(MainFormView, self).get_context_data(**kwargs)
        context["main_form"] = MainForm()
        return context


    def get(self, request):
        form = MainForm()
        return render(request, 'main_form.html', {'form': form})


class InfoListView(ListView):
    model = CodeList
    context_object_name = 'info'


class InfoCreateView(CreateView):
    model = CodeList
    fields = ('commodity_code_system', 'code_list')
    success_url = reverse_lazy('info_list_view')


class InfoUpdateView(UpdateView):
    model = CodeList
    fields = ('entities', 'commodity_code_system', 'code_list')
    success_url = reverse_lazy('info_list_view')
