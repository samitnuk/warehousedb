from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Tool, ToolChange
from ..forms import DateRangeForm

from ..helpers import get_date_range


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

            if range_start > range_stop:
                range_start, range_stop = range_stop, range_start

            date_range = get_date_range(range_start, range_stop)

            total_changes = ToolChange.objects.filter(
                changed_at__gte=range_start,
                changed_at__lte=range_stop)

            tools = Tool.objects.all()

            tools_list = []
            for tool in tools:
                tools_list.append(
                    [tool, total_changes.filter(tool=tool)])

            return render(
                request, 'items/tool_list_by_dates.html',
                {'date_range': date_range,
                 'tool_list': tool_list,
                 'form': form})

    range_stop = datetime.today()
    range_start = range_stop - timedelta(days=7)  # 7 days before today

    date_range = get_date_range(range_start, range_stop)

    total_changes = ToolChange.objects.filter(changed_at__gte=range_start,
                                              changed_at__lte=range_stop)

    tools = Tool.objects.all()

    tools_list = []
    for tool in tools:
        tools_list.append(
            [tools, total_changes.filter(tools=tools)])

    return render(
        request, 'items/tool_list_by_dates.html',
        {'initial_range_start': datetime.strftime(range_start, "%Y-%m-%d"),
         'initial_range_stop': datetime.strftime(range_stop, "%Y-%m-%d"),
         'date_range': date_range,
         'tool_list': tool_list,
         'form': form})


@login_required(login_url='/login/')
def tool_create(request):
    pass


@login_required(login_url='/login/')
def tool_delete(request, pk):
    pass


@login_required(login_url='/login/')
def tool_detail(request, pk):
    pass


@login_required(login_url='/login/')
def toolchange_detail(request, pk):
    pass


@login_required(login_url='/login/')
def toolchange_create(request):
    pass
