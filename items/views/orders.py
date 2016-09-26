from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Product, Order
from ..forms import AddOrderForm


@login_required(login_url='/login/')
def orders(request):
    orders_ = Order.objects.order_by('-order_date', '-id')

    return render(
        request, 'items/orders.html',
        {'orders': orders_})


@login_required(login_url='/login/')
def create_new_order(request):

    form = AddOrderForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            Order.objects.create(
                customer=form.cleaned_data['customer'],
                product=Product.objects.filter(
                    pk=form.cleaned_data['product']).first(),
                quantity=form.cleaned_data['quantity'])

            return redirect('orders')

        return render(
            request,
            'items/create_new_order.html',
            {'form': form})

    return render(
        request,
        'items/create_new_order.html',
        {'form': form})
