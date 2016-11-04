from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic import DeleteView
from django.views.generic import TemplateView

from ..models import Product
from ..forms import (AddProductForm, AddStdCableForm, AddTZACableForm,
                     AddBCableForm, AddHCableForm)


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


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('order_list')
    template_name = "items/object_confirm_delete.html"


class StdProductsList(TemplateView):
    template_name = 'items/std_products_list.html'


class StdCableCreate(FormView):
    template_name = 'items/product_create_std_cable.html'
    form_class = AddStdCableForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.create_std_cable()
        return super(StdCableCreate, self).form_valid(form)


class TZACableCreate(FormView):
    template_name = 'items/product_create_tza_cable.html'
    form_class = AddTZACableForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.create_tza_cable()
        return super(TZACableCreate, self).form_valid(form)


class BCableCreate(FormView):
    template_name = 'items/product_create_b_cable.html'
    form_class = AddBCableForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.create_b_cable()
        return super(BCableCreate, self).form_valid(form)


class HCableCreate(FormView):
    template_name = 'items/product_create_h_cable.html'
    form_class = AddHCableForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.create_h_cable()
        return super(HCableCreate, self).form_valid(form)
