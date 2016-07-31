from django.shortcuts import render

from .models import Item


def main(request):
    items = Item.objects.order_by('category')
    return render(request, 'items/main.html', {'items': items})
