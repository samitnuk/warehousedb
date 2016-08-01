from django.shortcuts import render

from .models import Item, Category


def main(request):
    items = Item.objects.order_by('category')
    categories = Category.objects.order_by('name')
    return render(request, 'items/main.html', {'items': items,
                                               'categories': categories})
