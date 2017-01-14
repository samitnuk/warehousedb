from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from ..models import Item, ItemChange, Category
from ..forms import DateRangeForm

from ..helpers import get_context_for_list_by_dates


class ItemList(ListView):
    model = Item
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super(ItemList, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        category_pk = self.kwargs.get('category_pk', None)
        if category_pk is None:
            active_category = categories.filter(special=False).first()
        else:
            active_category = categories.filter(pk=category_pk).first()
        context['active_category'] = active_category
        context['categories'] = categories
        context['items'] = Item.objects.filter(category=active_category)
        return context


class ItemListPrint(ListView):
    model = Item
    template_name = "items/item_list_print.html"

    def get_context_data(self, **kwargs):
        context = super(ItemListPrint, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        data = dict()
        for category in categories:
            data[category.title] = Item.objects.filter(category=category)
        context['data'] = sorted(data.items())
        return context


@login_required(login_url='/login/')
def list_by_dates(request):

    form = DateRangeForm(request.POST or None)

    range_start, range_stop = None, None

    if request.method == 'POST' and form.is_valid():
        range_start = form.cleaned_data['range_start']
        range_stop = form.cleaned_data['range_stop']

    context = get_context_for_list_by_dates(
        object_model=Item,
        objectchange_model=ItemChange,
        field_name='item',
        range_start=range_start,
        range_stop=range_stop)
    context['form'] = form
    return render(request, 'items/item_list_by_dates.html', context)


class ItemDetail(DetailView):
    model = Item
    context_object_name = 'item'


class ItemCreate(CreateView):
    model = Item
    fields = ['title', 'part_number', 'part_number2', 'picture', 'category',
              'rate', 'weight', 'critical_qty', 'notes']


class ItemUpdate(UpdateView):
    model = Item
    fields = ['title', 'part_number', 'part_number2', 'picture', 'category',
              'rate', 'weight', 'critical_qty', 'notes']


class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('item_list')
    template_name = "items/object_confirm_delete.html"


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


class ItemChangeUpdate(UpdateView):
    model = ItemChange
    fields = ['additional_quantity', 'material', 'notes']


class ItemChangeDelete(DeleteView):
    model = ItemChange
    success_url = reverse_lazy('item_list')
    template_name = "items/object_confirm_delete.html"
