from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Item, ItemChange, Category


@login_required(login_url='/login/')
def main(request):
    items = Item.objects.order_by('category', 'title', 'part_number')
    categories = Category.objects.order_by('name')

    return render(
        request, 'items/main.html',
        {'items': items,
         'categories': categories})


@login_required(login_url='/login/')
def items_by_categories(request, pk):

    categories = Category.objects.order_by('name')

    if pk is None:
        active_category = categories.first()
    else:
        active_category = categories.filter(pk=pk).first()

    items = Item.objects.filter(category=active_category)

    buttons_in_row = 6
    row, rows = [], []
    for i, category in enumerate(categories, 1):
        row.append(category)
        if not i % buttons_in_row or i == len(categories):
            rows.append(row)
            row = []

    return render(
        request, 'items/items_by_categories.html',
        {'items': items,
         'active_category_id': active_category.id,
         'rows': rows})


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
            return render(
                request, 'items/items_by_dates.html',
                {'errors': errors})

        total_changes = ItemChange.objects.filter(changed_at__gte=range_start,
                                                  changed_at__lte=range_stop)
        if range_start > range_stop:
            range_start, range_stop = range_stop, range_start
        date_range = []
        while range_start <= range_stop:
            date_range.append(range_start)
            range_start += timedelta(days=1)

        items = Item.objects.order_by('category')

        items_list = []
        for item in items:
            items_list.append([item, total_changes.filter(item=item)])

        return render(
            request, 'items/items_by_dates.html',
            {'date_range': date_range,
             'items_list': items_list})

    else:
        range_stop = datetime.today()
        range_start = range_stop - timedelta(days=7)  # 7 days before today
        date_range = []
        i = range_start
        while i <= range_stop:
            date_range.append(i)
            i += timedelta(days=1)

        total_changes = ItemChange.objects.filter(changed_at__gte=range_start,
                                                  changed_at__lte=range_stop)

        items = Item.objects.order_by('category')

        items_list = []
        for item in items:
            items_list.append([item, total_changes.filter(item=item)])

        return render(
            request, 'items/items_by_dates.html',
            {'initial_range_start': datetime.strftime(range_start, "%Y-%m-%d"),
             'initial_range_stop': datetime.strftime(range_stop, "%Y-%m-%d"),
             'date_range': date_range,
             'items_list': items_list})


@login_required(login_url='/login/')
def item_details(request, pk):
    item = Item.objects.filter(pk=pk).first()

    return render(
        request, 'items/item_details.html',
        {'item': item})


@login_required(login_url='/login/')
def item_change_details(request, pk):
    item_change = ItemChange.objects.filter(pk=pk).first()

    return render(
        request, 'items/item_change_details.html',
        {'item_change': item_change})


@login_required(login_url='/login/')
def add_item_change(request, pk):
    item = Item.objects.filter(pk=pk).first()
    if request.method == 'POST':
        additional_quantity = request.POST.get("additional_quantity", "") \
                                          .strip()
        error = ""
        if not additional_quantity:
            error = "Введіть кількість"
        else:
            try:
                additional_quantity = float(additional_quantity)
            except Exception:
                error = "Введіть число"

        if error:
            return render(
                request, 'items/add_item_change.html',
                {'error': error,
                 'item': item})
        else:
            ItemChange.objects.create(
                additional_quantity=additional_quantity,
                item=item,
                changed_at=datetime.today(),
                notes=request.POST.get("notes", "")
            )

            return redirect('main')

    return render(
        request, 'items/add_item_change.html',
        {'item': item})
