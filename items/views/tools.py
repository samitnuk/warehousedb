from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Tool, ToolChange


@login_required(login_url='/login/')
def tool_list(request):
    pass


@login_required(login_url='/login/')
def tool_detail(request, pk):
    pass


@login_required(login_url='/login/')
def tool_create(request):
    pass


@login_required(login_url='/login/')
def toolchange_detail(request, pk):
    pass


@login_required(login_url='/login/')
def toolchange_create(request, pk):
    pass
