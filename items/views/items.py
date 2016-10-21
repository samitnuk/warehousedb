from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Item, ItemChange, Category
from ..forms import DateRangeForm

from ..helpers import get_date_range, get_objects_list


@login_required(login_url='/login/')
def main(request):
    items = Item.objects.all()
    categories = Category.objects.all()

    return render(
        request, 'items/main.html',
        {'items': items,
         'categories': categories})


@login_required(login_url='/login/')
def item_list_by_categories(request, pk):

    categories = Category.objects.all()

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
        request, 'items/item_list_by_categories.html',
        {'items': items,
         'active_category_id': active_category.id,
         'rows': rows})


@login_required(login_url='/login/')
def item_list_by_dates(request):

    form = DateRangeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            range_start = form.cleaned_data['range_start']
            range_stop = form.cleaned_data['range_stop']

            items_list = get_objects_list(
                range_start=range_start,
                range_stop=range_stop,
                object_model=Item,
                objectchange_model=ItemChange,
                field_name='item'
            )

            return render(
                request, 'items/item_list_by_dates.html',
                {'date_range': get_date_range(range_start, range_stop),
                 'items_list': items_list,
                 'form': form})

    range_stop = datetime.today()
    range_start = range_stop - timedelta(days=7)  # 7 days before today

    items_list = get_objects_list(
        range_start=range_start,
        range_stop=range_stop,
        object_model=Item,
        objectchange_model=ItemChange,
        field_name='item'
    )

    return render(
        request, 'items/item_list_by_dates.html',
        {'initial_range_start': datetime.strftime(range_start, "%Y-%m-%d"),
         'initial_range_stop': datetime.strftime(range_stop, "%Y-%m-%d"),
         'date_range': get_date_range(range_start, range_stop),
         'items_list': items_list,
         'form': form})


@login_required(login_url='/login/')
def item_detail(request, pk):
    item = Item.objects.filter(pk=pk).first()

    return render(
        request, 'items/item_detail.html',
        {'item': item})


@login_required(login_url='/login/')
def itemchange_detail(request, pk):
    item_change = ItemChange.objects.filter(pk=pk).first()

    return render(
        request, 'items/itemchange_detail.html',
        {'item_change': item_change})


@login_required(login_url='/login/')
def itemchange_create(request, pk):
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
                request, 'items/itemchange_create.html',
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
        request, 'items/itemchange_create.html',
        {'item': item})
