from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Material, MaterialChange


@login_required(login_url='/login/')
def material_list(request):
    pass


@login_required(login_url='/login/')
def material_detail(request, pk):
    pass


@login_required(login_url='/login/')
def material_create(request):
    pass


@login_required(login_url='/login/')
def materialchange_detail(request, pk):
    pass


@login_required(login_url='/login/')
def materialchange_create(request, pk):
    pass
