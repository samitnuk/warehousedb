from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from .models import Item, Category


@login_required(login_url='/login/')
def main(request):
    items = Item.objects.order_by('category')
    categories = Category.objects.order_by('name')
    return render(request, 'items/main.html', {'items': items,
                                               'categories': categories})


@login_required(login_url='/login/')
def category(request, pk):
    category = Category.objects.filter(pk=pk).first()
    items = Item.objects.filter(category=category)
    print(category.name)
    return render(request, 'items/category.html', {'items': items,
                                                   'category': category})


@login_required(login_url='/login/')
def items_by_dates(request):
    return HttpResponse('<h1>Items by dates page</h1>')


@login_required(login_url='/login/')
def item_details(request, pk):
    item = Item.objects.filter(pk=pk).first()
    return render(request, 'items/item_details.html', {'item': item})


def login(request):
    return HttpResponse('<h1>LOGIN page</h1>')


@login_required(login_url='/login/')
def logout(request):
    logout_user(request)
    return redirect('main')
