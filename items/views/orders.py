from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Order


@login_required(login_url='/login/')
def orders(request):
    orders = Order.objects.all()

    return render(
        request, 'items/orders.html',
        {'orders': orders})
