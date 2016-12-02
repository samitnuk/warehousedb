from datetime import datetime, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse

from ..models import Material, MaterialChange
from ..forms import DateRangeForm

from ..helpers import get_date_range, get_objects_list


class MaterialList(ListView):
    model = Material
    context_object_name = 'materials'


@login_required(login_url='/login/')
def list_by_dates(request):

    form = DateRangeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        range_start = form.cleaned_data['range_start']
        range_stop = form.cleaned_data['range_stop']

        materials_list = get_objects_list(
            range_start=range_start,
            range_stop=range_stop,
            object_model=Material,
            objectchange_model=MaterialChange,
            field_name='material')

        return render(
            request, 'items/material_list_by_dates.html',
            {'date_range': get_date_range(range_start, range_stop),
             'material_list': materials_list,
             'form': form})

    range_stop = datetime.today()
    range_start = range_stop - timedelta(days=7)

    materials_list = get_objects_list(
        range_start=range_start,
        range_stop=range_stop,
        object_model=Material,
        objectchange_model=MaterialChange,
        field_name='material')

    return render(
        request, 'items/material_list_by_dates.html',
        {'initial_range_start': datetime.strftime(range_start, "%Y-%m-%d"),
         'initial_range_stop': datetime.strftime(range_stop, "%Y-%m-%d"),
         'date_range': get_date_range(range_start, range_stop),
         'material_list': materials_list,
         'form': form})


class MaterialDetail(DetailView):
    model = Material
    template_name = 'items/object_detail.html'

    def url_for_update(self):
        return reverse('material_update', kwargs={'pk': self.kwargs['pk']})

    def url_for_delete(self):
        return reverse('material_delete', kwargs={'pk': self.kwargs['pk']})


class MaterialCreate(CreateView):
    model = Material
    fields = ['title', 'critical_qty', 'notes']
    template_name = 'items/object_form.html'
    success_url = reverse_lazy('material_list')

    @staticmethod
    def page_name():
        return "Створити матеріал"


class MaterialUpdate(UpdateView):
    model = Material
    fields = ['title', 'critical_qty', 'notes']
    template_name = 'items/object_form.html'

    @staticmethod
    def page_name():
        return "Редагувати матеріал"


class MaterialDelete(DeleteView):
    model = Material
    success_url = reverse_lazy('material_list')
    template_name = "items/object_confirm_delete.html"


class MaterialChangeDetail(DetailView):
    model = MaterialChange
    context_object_name = 'materialchange'


class MaterialChangeCreate(CreateView):
    model = MaterialChange
    fields = ['additional_quantity', 'notes']
    template_name = 'items/objectchange_form.html'
    success_url = reverse_lazy('material_list')

    def post(self, request, *args, **kwargs):
        # self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        form.instance.material = Material.objects.filter(
            pk=self.kwargs['material_pk']).first()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        return {'object': Material.objects.filter(
            pk=self.kwargs['material_pk']).first()}


class MaterialChangeDelete(DeleteView):
    model = MaterialChange
    success_url = reverse_lazy('material_list')
    template_name = "items/object_confirm_delete.html"
