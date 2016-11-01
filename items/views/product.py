from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from ..models import Item, Product, Component
from ..forms import (AddProductForm, AddStdCableForm, AddTZACableForm,
                     AddBCableForm, AddHCableForm)


class ProductList(ListView):
    model = Product
    context_object_name = 'products'


@login_required(login_url='/login/')
def list_(request):
    context = {'products': Product.objects.all()}

    return render(request, 'items/product_list.html', context)


@login_required(login_url='/login/')
def detail(request, pk):
    context = {'product': Product.objects.filter(pk=pk).first()}

    return render(request, 'items/product_detail.html', context)


@login_required(login_url='/login/')
def create(request):

    form = AddProductForm(request.POST or None)

    items = Item.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            product = Product.objects.create(
                title=form.cleaned_data['title'],
                part_number=form.cleaned_data['part_number'],
                notes=form.cleaned_data['notes'])

            for item in items:
                quantity = form.cleaned_data['item_{}'.format(item.id)]
                if quantity is not None and float(quantity) > 0:
                    Component.objects.create(product=product,
                                             item=item,
                                             quantity=quantity,)

            return redirect('product_list')

        else:
            context = {'items': items, 'form': form}
            return render(request, 'items/product_create.html', context)

    context = {'items': items, 'form': form}
    return render(request, 'items/product_create.html', context)


@login_required(login_url='/login/')
def delete(request, pk):
    pass


class StdCableCreate(FormView):
    template_name = 'items/product_create_std_cable.html'
    form_class = AddStdCableForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.create_std_cable()
        return super(StdCableCreate, self).form_valid(form)


class TZACableCreate(FormView):
    template_name = 'items/product_create_tza_cable.html'
    form_class = AddTZACableForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.create_tza_cable()
        return super(TZACableCreate, self).form_valid(form)


class BCableCreate(FormView):
    template_name = 'items/product_create_b_cable.html'
    form_class = AddBCableForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.create_b_cable()
        return super(BCableCreate, self).form_valid(form)


@login_required(login_url='/login/')
def create_h_cable(request):
    # utils.create_h_cable()
    pass


class HCableCreate(FormView):
    template_name = 'items/product_create_h_cable.html'
    form_class = AddHCableForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.create_h_cable()
        return super(HCableCreate, self).form_valid(form)