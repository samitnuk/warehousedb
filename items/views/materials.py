from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Material, MaterialChange
from ..forms import DateRangeForm

from ..helpers import get_date_range


@login_required(login_url='/login/')
def material_list(request):
    materials = Material.objects.all()

    return render(
        request, 'items/material_list.html',
        {'materials': materials})


@login_required(login_url='/login/')
def material_list_by_dates(request):

    form = DateRangeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            range_start = form.cleaned_data['range_start']
            range_stop = form.cleaned_data['range_stop']

            if range_start > range_stop:
                range_start, range_stop = range_stop, range_start

            date_range = get_date_range(range_start, range_stop)

            total_changes = MaterialChange.objects.filter(
                changed_at__gte=range_start,
                changed_at__lte=range_stop)

            materials = Material.objects.all()

            materials_list = []
            for material in materials:
                materials_list.append(
                    [material, total_changes.filter(material=material)])

            return render(
                request, 'items/material_list_by_dates.html',
                {'date_range': date_range,
                 'material_list': material_list,
                 'form': form})

    range_stop = datetime.today()
    range_start = range_stop - timedelta(days=7)  # 7 days before today

    date_range = get_date_range(range_start, range_stop)

    total_changes = MaterialChange.objects.filter(changed_at__gte=range_start,
                                                  changed_at__lte=range_stop)

    materials = Material.objects.all()

    materials_list = []
    for material in materials:
        materials_list.append(
            [materials, total_changes.filter(materials=materials)])

    return render(
        request, 'items/material_list_by_dates.html',
        {'initial_range_start': datetime.strftime(range_start, "%Y-%m-%d"),
         'initial_range_stop': datetime.strftime(range_stop, "%Y-%m-%d"),
         'date_range': date_range,
         'material_list': material_list,
         'form': form})


@login_required(login_url='/login/')
def material_create(request):
    pass


@login_required(login_url='/login/')
def material_delete(request, pk):
    pass


@login_required(login_url='/login/')
def material_detail(request, pk):
    pass


@login_required(login_url='/login/')
def materialchange_detail(request, pk):
    pass


@login_required(login_url='/login/')
def materialchange_create(request, pk):
    pass
