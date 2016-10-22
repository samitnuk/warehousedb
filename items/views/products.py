from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Item, Product, Component
from ..forms import (AddProductForm, AddStdCableForm, AddTZACableForm,
                     AddBCableForm)
from ..utils import create_std_cable, create_tza_cable, create_B_cable


@login_required(login_url='/login/')
def product_list(request):
    products_ = Product.objects.all()

    return render(
        request, 'items/product_list.html',
        {'products': products_})


@login_required(login_url='/login/')
def product_detail(request, pk):
    product = Product.objects.filter(pk=pk).first()

    return render(
        request, 'items/product_detail.html',
        {'product': product})


@login_required(login_url='/login/')
def product_create(request):

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
            return render(
                request,
                'items/product_create.html',
                {'items': items, 'form': form})

    return render(
        request, 'items/product_create.html',
        {'items': items, 'form': form})


@login_required(login_url='/login/')
def product_delete(request, pk):
    pass


@login_required(login_url='/login/')
def product_create_std_cable(request):

    form = AddStdCableForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            create_std_cable(
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

        return render(
            request, 'items/product_create_std_cable.html',
            {'form': form})

    return render(
        request, 'items/product_create_std_cable.html',
        {'form': form})


@login_required(login_url='/login/')
def product_create_tza_cable(request):

    form = AddTZACableForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            create_tza_cable(
                conduit_id=form.cleaned_data['conduit'],
                core_id=form.cleaned_data['core'],
                is_st_rods=form.cleaned_data['is_st_rods'],
                length=form.cleaned_data['length'])

            return redirect('product_list')

        return render(
            request, 'items/product_create_tza_cable.html',
            {'form': form})

    return render(
        request, 'items/product_create_tza_cable.html',
        {'form': form})


@login_required(login_url='/login/')
def product_create_b_cable(request):

    form = AddBCableForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            create_B_cable(
                cable_type=form.cleaned_data['cable_type'],
                conduit_id=form.cleaned_data['conduit'],
                core_id=form.cleaned_data['core'],
                is_st_rods=form.cleaned_data['is_st_rods'],
                is_st_sleeves=form.cleaned_data['is_st_sleeves'],
                length=form.cleaned_data['length'])

            return redirect('product_list')

        return render(
            request, 'items/product_create_b_cable.html',
            {'form': form})

    return render(
        request, 'items/product_create_b_cable.html',
        {'form': form})


@login_required(login_url='/login/')
def product_create_h_cable(request):
    pass
