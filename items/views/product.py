from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Item, Product, Component


@login_required(login_url='/login/')
def create_new_product(request):
    if request.method == 'POST':

        errors = {}

        product_title = request.POST.get("product_title", "").strip()
        if not product_title:
            errors["product_title"] = "Найменування обов'язкове"
            return render(request, 'items/create_new_product.html',
                          {'errors': errors})

        product_part_number = request.POST.get("product_part_number", "").strip()
        product_notes = request.POST.get("product_notes", "")

        product = Product.objects.create(title=product_title,
                                         part_number=product_part_number,
                                        notes=product_notes)

        items = Item.objects.all()

        for item in items:
            quantity_str = request.POST.get('item_%s' % item.id, "").strip()
            if quantity_str:
                try:
                    quantity = float(quantity_str)
                    component = Component(product=product,
                                          item=item,
                                          quantity=quantity)
                    component.save()
                except ValueError:
                    errors['item_%s' % item.id] = "ВВодити тільки числа"

    return render(request, 'items/create_new_product.html', {})
