from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic import DeleteView
from django.views.generic import TemplateView

from ..models import Product, Category
from ..forms import (AddProductForm, AddStdCableForm, AddStdTCableForm,
                     AddTZACableForm, AddBCableForm, AddHCableForm)


class ProductList(ListView):
    model = Product
    context_object_name = 'products'


class ProductDetail(DetailView):
    model = Product


class ProductCreate(FormView):
    template_name = 'items/product_form.html'
    form_class = AddProductForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.create_product()
        return super(ProductCreate, self).form_valid(form)

    def categories(self):
        return Category.objects.all()


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
    template_name = "items/object_confirm_delete.html"


class StdProductsList(TemplateView):
    template_name = 'items/std_products_list.html'


class StdProductCreate(FormView):
    STD_PRODUCTS = {
        0: {
            'template_name': 'items/std_products/create_std_cable.html',
            'form_class': AddStdCableForm},
        1: {
            'template_name': 'items/std_products/create_std_t_cable.html',
            'form_class': AddStdTCableForm},
        2: {
            'template_name': 'items/std_products/create_tza_cable.html',
            'form_class': AddTZACableForm},
        3: {
            'template_name': 'items/std_products/create_b_cable.html',
            'form_class': AddBCableForm},
        4: {
            'template_name': 'items/std_products/create_h_cable.html',
            'form_class': AddHCableForm},
    }

    success_url = reverse_lazy('product_list')

    def dispatch(self, request, *args, **kwargs):
        product = self.STD_PRODUCTS[int(self.kwargs['product_num'])]
        self.template_name = product['template_name']
        self.form_class = product['form_class']

        return super(StdProductCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.create_product()
        return super(StdProductCreate, self).form_valid(form)
