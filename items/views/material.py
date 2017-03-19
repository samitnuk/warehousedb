from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from ..forms import DateRangeForm
from ..helpers import get_context_for_list_by_dates
from ..models import Material, MaterialChange


class MaterialList(ListView):
    model = Material
    context_object_name = 'materials'


@login_required(login_url='/login/')
def list_by_dates(request):

    form = DateRangeForm(request.POST or None)

    range_start, range_stop = None, None

    if request.method == 'POST' and form.is_valid():
        range_start = form.cleaned_data['range_start']
        range_stop = form.cleaned_data['range_stop']

    context = get_context_for_list_by_dates(
        object_model=Material,
        objectchange_model=MaterialChange,
        field_name='material',
        range_start=range_start,
        range_stop=range_stop)
    context['form'] = form
    return render(request, 'items/material_list_by_dates.html', context)


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


class MaterialChangeUpdate(UpdateView):
    model = MaterialChange
    fields = ['additional_quantity', 'notes']
    template_name = 'items/object_form.html'

    def page_name(self):
        materialchange = MaterialChange.objects.filter(
            pk=self.kwargs['pk']).first()
        return 'Редагувати зміну кількості {}'.format(
            materialchange.material)


class MaterialChangeDelete(DeleteView):
    model = MaterialChange
    success_url = reverse_lazy('material_list')
    template_name = "items/object_confirm_delete.html"
