from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required

from .models import Item, Category


@login_required(login_url='/login/')
def main(request):
    items = Item.objects.order_by('category')
    categories = Category.objects.order_by('name')
    return render(request, 'items/main.html', {'items': items,
                                               'categories': categories})


@login_required(login_url='/login/')
def category(request):
    pass


@login_required(login_url='/login/')
def items_by_dates(request):
    pass


@login_required(login_url='/login/')
def item_details(request):
    pass


def login(request):
    pass


@login_required(login_url='/login/')
def login(request):
    logout_user(request)
    return redirect('main')
