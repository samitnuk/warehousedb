from datetime import datetime, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView  # DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from ..models import Item, ItemChange, Category
from ..forms import DateRangeForm

from ..helpers import get_date_range, get_objects_list


class ItemList(ListView):
    model = Item
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super(ItemList, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        category_pk = self.kwargs.get('category_pk', None)
        if category_pk is None:
            active_category = categories.first()
        else:
            active_category = categories.filter(pk=category_pk).first()
        context['active_category_id'] = active_category.id
        context['categories'] = categories
        context['items'] = Item.objects.filter(category=active_category)
        return context


# @login_required(login_url='/login/')
# def list_by_categories(request, category_pk):
#
#     categories = Category.objects.all()
#
#     if category_pk is None:
#         active_category = categories.first()
#     else:
#         active_category = categories.filter(pk=category_pk).first()
#
#     context = {
#         'items': Item.objects.filter(category=active_category),
#         'active_category_id': active_category.id,
#         'categories': categories}
#
#     return render(request, 'items/item_list_by_categories.html', context)


@login_required(login_url='/login/')
def list_by_dates(request):

    form = DateRangeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        range_start = form.cleaned_data['range_start']
        range_stop = form.cleaned_data['range_stop']

        items_list = get_objects_list(
            range_start=range_start,
            range_stop=range_stop,
            object_model=Item,
            objectchange_model=ItemChange,
            field_name='item')

        context = {
            'date_range': get_date_range(range_start, range_stop),
            'items_list': items_list,
            'form': form}

        return render(request, 'items/item_list_by_dates.html', context)

    range_stop = datetime.today()
    range_start = range_stop - timedelta(days=7)  # 7 days before today

    items_list = get_objects_list(
        range_start=range_start,
        range_stop=range_stop,
        object_model=Item,
        objectchange_model=ItemChange,
        field_name='item')

    context = {
        'initial_range_start': datetime.strftime(range_start, "%Y-%m-%d"),
        'initial_range_stop': datetime.strftime(range_stop, "%Y-%m-%d"),
        'date_range': get_date_range(range_start, range_stop),
        'items_list': items_list,
        'form': form}

    return render(request, 'items/item_list_by_dates.html', context)


class ItemDetail(DetailView):
    model = Item
    context_object_name = 'item'


class ItemCreate(CreateView):
    model = Item
    fields = ['title', 'part_number', 'part_number2', 'picture', 'category',
              'rate', 'weight', 'notes']
    success_url = reverse_lazy('item_list')


class ItemChangeDetail(DetailView):
    model = ItemChange
    context_object_name = 'item_change'


class ItemChangeCreate(CreateView):
    model = ItemChange
    fields = ['additional_quantity', 'material', 'notes']
    # template_name = 'items/itemchange_form.html'
    success_url = reverse_lazy('item_list')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        item_pk = self.kwargs['item_pk']
        form.instance.item = Item.objects.filter(pk=item_pk).first()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        item_pk = self.kwargs['item_pk']
        return {'item': Item.objects.filter(pk=item_pk).first()}
