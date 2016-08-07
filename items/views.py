from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from .models import Item, ItemChange, Category


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
    if request.method == 'POST':
        
        errors = {}
        
        range_start = request.POST.get("range_start", "").strip()
        if not range_start:
            errors["range_start"] = "Дата є обов'язковою"
        else:
            try:
                range_start = datetime.strptime(range_start, "%Y-%m-%d")
            except Exception:
                errors["range_start"] = \
                    "Введіть коректний формат дати (напр. 2016-08-01)"

        range_stop = request.POST.get("range_stop", "").strip()
        if not range_stop:
            errors["range_stop"] = "Дата є обов'язковою"
        else:
            try:
                range_stop = datetime.strptime(range_stop, "%Y-%m-%d")
            except Exception:
                errors["range_stop"] = \
                    "Введіть коректний формат дати (напр. 2016-08-01)"

        if errors:
            return render(request, 'items/items_by_dates.html', {'errors': errors})

        total_changes = ItemChange.objects.filter(changed_at__gte=range_start, changed_at__lte=range_stop)
        if range_start > range_stop:
            range_start, range_stop = range_stop, range_start
        date_range = []
        step = timedelta(days=1)
        while range_start <= range_stop:
            date_range.append(range_start)
            range_start += timedelta(days=1)

        items = Item.objects.order_by('category')

        return render(request, 'items/items_by_dates.html',
                      {'date_range':date_range,
                       'items':items,
                       'total_changes':total_changes})

    else:
        return render(request, 'items/items_by_dates.html', {})


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
