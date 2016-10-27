from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from ..models import Material, MaterialChange
from ..forms import DateRangeForm

from ..helpers import get_date_range, get_objects_list


@login_required(login_url='/login/')
def list_(request):
    materials = Material.objects.all()

    return render(
        request, 'items/material_list.html',
        {'materials': materials})


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
            field_name='material',
        )

        return render(
            request, 'items/material_list_by_dates.html',
            {'date_range': get_date_range(range_start, range_stop),
             'material_list': materials_list,
             'form': form},
        )

    range_stop = datetime.today()
    range_start = range_stop - timedelta(days=7)  # 7 days before today

    materials_list = get_objects_list(
        range_start=range_start,
        range_stop=range_stop,
        object_model=Material,
        objectchange_model=MaterialChange,
        field_name='material',
    )

    return render(
        request, 'items/material_list_by_dates.html',
        {'initial_range_start': datetime.strftime(range_start, "%Y-%m-%d"),
         'initial_range_stop': datetime.strftime(range_stop, "%Y-%m-%d"),
         'date_range': get_date_range(range_start, range_stop),
         'material_list': materials_list,
         'form': form},
    )


@login_required(login_url='/login/')
def detail(request, pk):

    return render(
        request, 'items/material_detail.html',
        {'material': Material.objects.filter(pk=pk).first()},
    )


class MaterialCreate(CreateView):
    model = Material
    fields = ['title', 'notes']


@login_required(login_url='/login/')
def delete(request, pk):
    Material.objects.filter(pk=pk).delete()

    return redirect('material_list')


@login_required(login_url='/login/')
def materialchange_detail(request, pk):

    return render(
        request, 'items/materialchange_detail.html',
        {'materialchange': MaterialChange.objects.filter(pk=pk).first()}
    )


@login_required(login_url='/login/')
def materialchange_create(request, pk):
    pass


@login_required(login_url='/login/')
def materialchange_delete(request, pk):
    MaterialChange.objects.filter(pk=pk).delete()

    return redirect('material_list_by_dates')
