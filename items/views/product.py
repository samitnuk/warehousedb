from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from ..models import Item, Product, Component
from ..forms import (AddProductForm, AddStdCableForm, AddTZACableForm,
                     AddBCableForm)
from items import utils


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


@login_required(login_url='/login/')
def create_std_cable(request):

    form = AddStdCableForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            utils.create_std_cable(
                conduit_id=form.cleaned_data['conduit'],
                core_id=form.cleaned_data['core'],
                serie=form.cleaned_data['serie'],
                travel=form.cleaned_data['travel'],
                mounting=form.cleaned_data['mounting'],
                is_st_rods=form.cleaned_data['is_st_rods'],
                is_st_sleeves=form.cleaned_data['is_st_sleeves'],
                is_plastic_sleeves=form.cleaned_data['is_plastic_sleeves'],
                length=form.cleaned_data['length'])

            return redirect('product_list')

        context = {'form': form}
        return render(request, 'items/product_create_std_cable.html', context)

    context = {'form': form}
    return render(request, 'items/product_create_std_cable.html', context)


@login_required(login_url='/login/')
def create_tza_cable(request):

    form = AddTZACableForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            utils.create_tza_cable(
                conduit_id=form.cleaned_data['conduit'],
                core_id=form.cleaned_data['core'],
                is_st_rods=form.cleaned_data['is_st_rods'],
                length=form.cleaned_data['length'])

            return redirect('product_list')

        context = {'form': form}
        return render(request, 'items/product_create_tza_cable.html', context)

    context = {'form': form}
    return render(request, 'items/product_create_tza_cable.html', context)


@login_required(login_url='/login/')
def create_b_cable(request):

    form = AddBCableForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            utils.create_B_cable(
                cable_type=form.cleaned_data['cable_type'],
                conduit_id=form.cleaned_data['conduit'],
                core_id=form.cleaned_data['core'],
                is_st_rods=form.cleaned_data['is_st_rods'],
                is_st_sleeves=form.cleaned_data['is_st_sleeves'],
                length=form.cleaned_data['length'])

            return redirect('product_list')

        context = {'form': form}
        return render(request, 'items/product_create_b_cable.html', context)

    context = {'form': form}
    return render(request, 'items/product_create_b_cable.html', context)


@login_required(login_url='/login/')
def create_h_cable(request):
    # utils.create_h_cable()
    pass
