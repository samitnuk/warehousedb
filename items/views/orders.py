from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Product, Order
from ..forms import AddOrderForm


@login_required(login_url='/login/')
def orders(request):
    orders_ = Order.objects.order_by('-order_date')

    return render(
        request, 'items/orders.html',
        {'orders': orders_})


@login_required(login_url='/login/')
def create_new_order(request):

    if request.method == 'POST':
        form = AddOrderForm(request.POST)
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

    form = AddOrderForm()

    return render(
        request,
        'items/create_new_order.html',
        {'form': form})
