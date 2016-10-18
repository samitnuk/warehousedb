from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Product, Order
from ..forms import AddOrderForm


@login_required(login_url='/login/')
def order_list(request):
    orders_ = Order.objects.all()

    return render(
        request, 'items/order_list.html',
        {'orders': orders_})


@login_required(login_url='/login/')
def order_create(request):

    form = AddOrderForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            Order.objects.create(
                customer=form.cleaned_data['customer'],
                product=Product.objects.filter(
                    pk=form.cleaned_data['product']).first(),
                quantity=form.cleaned_data['quantity'])

            return redirect('order_list')

        return render(
            request,
            'items/order_create.html',
            {'form': form})

    return render(
        request,
        'items/order_create.html',
        {'form': form})
