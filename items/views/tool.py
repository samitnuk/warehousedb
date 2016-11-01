from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse

from ..models import Tool, ToolChange
from ..forms import DateRangeForm

from ..helpers import get_date_range, get_objects_list


@login_required(login_url='/login/')
def list_(request):
    context = {'tools': Tool.objects.all()}
    return render(request, 'items/tool_list.html', context)


@login_required(login_url='/login/')
def list_by_dates(request):

    form = DateRangeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        range_start = form.cleaned_data['range_start']
        range_stop = form.cleaned_data['range_stop']

        context = {
            'form': form,
            'date_range': get_date_range(range_start, range_stop),
            'tools_list': get_objects_list(range_start=range_start,
                                           range_stop=range_stop,
                                           object_model=Tool,
                                           objectchange_model=ToolChange,
                                           field_name='tool')}

        return render(request, 'items/tool_list_by_dates.html', context)

    range_stop = datetime.today()
    range_start = range_stop - timedelta(days=7)

    context = {
        'form': form,
        'initial_range_start': datetime.strftime(range_start, "%Y-%m-%d"),
        'initial_range_stop': datetime.strftime(range_stop, "%Y-%m-%d"),
        'date_range': get_date_range(range_start, range_stop),
        'tools_list': get_objects_list(range_start=range_start,
                                       range_stop=range_stop,
                                       object_model=Tool,
                                       objectchange_model=ToolChange,
                                       field_name='tool')}

    return render(request, 'items/tool_list_by_dates.html', context)


class ToolDetail(DetailView):
    model = Tool
    template_name = 'items/object_detail.html'

    def url_for_update(self):
        return reverse('tool_update', kwargs={'pk': self.kwargs['pk']})

    def url_for_delete(self):
        return reverse('tool_delete', kwargs={'pk': self.kwargs['pk']})


class ToolCreate(CreateView):
    model = Tool
    fields = ['title', 'notes']
    template_name = 'items/object_form.html'
    success_url = reverse_lazy('tool_list')

    @staticmethod
    def page_name():
        return "Створити інструмент"


class ToolUpdate(UpdateView):
    model = Tool
    fields = ['title', 'notes']
    template_name = 'items/object_form.html'

    @staticmethod
    def page_name():
        return "Редагувати інструмент"


class ToolDelete(DeleteView):
    model = Tool
    success_url = reverse_lazy('tool_list')
    template_name = "items/object_confirm_delete.html"


@login_required(login_url='/login/')
def toolchange_detail(request, pk):

    return render(
        request, 'items/toolchange_detail.html',
        {'toolchange': ToolChange.objects.filter(pk=pk).first()}
    )


class ToolChangeCreate(CreateView):
    model = ToolChange
    fields = ['additional_quantity', 'notes']
    template_name = 'items/objectchange_form.html'
    success_url = reverse_lazy('tool_list')

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # the actual modification of the form
        form.instance.tool = Tool.objects.filter(
            pk=self.kwargs['tool_pk']).first()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        return {'object': Tool.objects.filter(
            pk=self.kwargs['tool_pk']).first()}


class ToolChangeDelete(DeleteView):
    model = ToolChange
    success_url = reverse_lazy('tool_list')
    template_name = "items/object_confirm_delete.html"
