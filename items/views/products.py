from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Item, Product, Component
from ..forms import AddProductForm, AddStdCableForm
from ..utils import create_std_cable


@login_required(login_url='/login/')
def create_new_product(request):

    items = Item.objects.all()

    if request.method == 'POST':
        form = AddProductForm(request.POST)
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

            return redirect('products')

        else:
            return render(
                request,
                'items/create_new_product.html',
                {'items': items, 'form': form})

    # if GET or any other method
    else:
        form = AddProductForm(auto_id=False)

        return render(
            request, 'items/create_new_product.html',
            {'items': items, 'form': form})


@login_required(login_url='/login/')
def products(request):
    products_ = Product.objects.order_by('-id')

    return render(
        request, 'items/products.html',
        {'products': products_})


@login_required(login_url='/login/')
def product_details(request, pk):
    product = Product.objects.filter(pk=pk).first()

    return render(
        request, 'items/product_details.html',
        {'product': product})


@login_required(login_url='/login/')
def add_std_cable(request):

    if request.method == 'POST':
        form = AddStdCableForm(request.POST)
        if form.is_valid():
            conduit_id = form.cleaned_data['conduit']
            core_id = form.cleaned_data['core']
            serie = form.cleaned_data['serie']
            travel = form.cleaned_data['travel']
            mounting = form.cleaned_data['mounting']
            length = form.cleaned_data['length']

            create_std_cable(
                core_id, conduit_id, serie, travel, mounting, length)

            return redirect('products')

        return render(
            request, 'items/add_std_cable.html',
            {'form': form})

    form = AddStdCableForm()

    return render(
        request, 'items/add_std_cable.html',
        {'form': form})
