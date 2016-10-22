from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Tool, ToolChange
from ..forms import DateRangeForm

from ..helpers import get_date_range, get_objects_list


@login_required(login_url='/login/')
def tool_list(request):
    tool = Tool.objects.all()

    return render(
        request, 'items/tool_list.html',
        {'tool': tool})


@login_required(login_url='/login/')
def tool_list_by_dates(request):

    form = DateRangeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            range_start = form.cleaned_data['range_start']
            range_stop = form.cleaned_data['range_stop']

            tools_list = get_objects_list(
                range_start=range_start,
                range_stop=range_stop,
                object_model=Tool,
                objectchange_model=ToolChange,
                field_name='tool'
            )

            return render(
                request, 'items/tool_list_by_dates.html',
                {'date_range': get_date_range(range_start, range_stop),
                 'tools_list': tools_list,
                 'form': form})

    range_stop = datetime.today()
    range_start = range_stop - timedelta(days=7)  # 7 days before today

    tools_list = get_objects_list(
        range_start=range_start,
        range_stop=range_stop,
        object_model=Tool,
        objectchange_model=ToolChange,
        field_name='tool'
    )

    return render(
        request, 'items/tool_list_by_dates.html',
        {'initial_range_start': datetime.strftime(range_start, "%Y-%m-%d"),
         'initial_range_stop': datetime.strftime(range_stop, "%Y-%m-%d"),
         'date_range': get_date_range(range_start, range_stop),
         'tools_list': tools_list,
         'form': form})


@login_required(login_url='/login/')
def tool_detail(request, pk):
    pass


@login_required(login_url='/login/')
def tool_create(request):
    pass


@login_required(login_url='/login/')
def tool_delete(request, pk):
    pass


@login_required(login_url='/login/')
def toolchange_detail(request, pk):
    pass


@login_required(login_url='/login/')
def toolchange_create(request):
    pass


@login_required(login_url='/login/')
def toolchange_delete(request):
    pass
