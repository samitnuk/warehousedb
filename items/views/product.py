from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Item, Product, Component
from ..forms import AddProductForm


@login_required(login_url='/login/')
def create_new_product(request):

    items = Item.objects.all()
    
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = Product.objects.create(
                title=form.cleaned_data['title'],
                part_number=form.cleaned_data['part_number'],
                notes=form.cleaned_data['notes'],
            )

            for item in items:
                quantity = form.cleaned_data['item_%s' % item.id]
                print(quantity)
                if quantity is not None and float(quantity) > 0:
                    component = Component.objects.create(
                        product=product,
                        item=item,
                        quantity=quantity,
                    )

            return redirect('main')

        else:
            return render(request, 'items/create_new_product.html', 
                {'items': items, 'form': form}
            )

    # if GET or any other method
    else:
        form = AddProductForm(auto_id=False)
        return render(request, 'items/create_new_product.html', 
            {'items': items, 'form': form}
        )

        # errors = {}

        # product_title = request.POST.get("product_title", "").strip()
        # if not product_title:
        #     errors["product_title"] = "Найменування обов'язкове"

        # quantity = {}
        # for item in items:
        #     quantity_str = request.POST.get("%s" % item.id, "").strip()
        #     if quantity_str:
        #         try:
        #             quantity["%s" % item.id] = float(quantity_str)
        #         except ValueError:
        #             errors[item.id] = "Вводити тільки числа"

        # if errors:
        #     return render(request, 'items/create_new_product.html',
        #                   {'items': items,
        #                    'errors': errors})
        # else:
        #     product_part_number = request.POST \
        #                                  .get("product_part_number", "") \
        #                                  .strip()
        #     product_notes = request.POST.get("product_notes", "").strip()
        #     product = Product.objects.create(title=product_title,
        #                                      part_number=product_part_number,
        #                                      notes=product_notes)
        #     for item in items:
        #         if quantity["%s" % item.id] > 0:
        #             component = Component(product=product,
        #                                   item=item,
        #                                   quantity=quantity[item.id])
        #             component.save()

    # return render(request, 'items/create_new_product.html',
    #               {'items': items})

@login_required(login_url='/login/')
def products(request):
    pass