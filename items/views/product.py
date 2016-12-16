from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic import DeleteView
from django.views.generic import TemplateView

from ..models import Product
from ..forms import AddProductForm
from ..std_products import STD_PRODUCTS
from ..utils import create_ptz_shifter_


class ProductList(ListView):
    model = Product
    context_object_name = 'products'


class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        product = self.get_object()
        context['components'] = product.components.order_by('item__title')
        return context


class ProductCreate(FormView):
    template_name = 'items/product_form.html'
    form_class = AddProductForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.create_product()
        return super(ProductCreate, self).form_valid(form)


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
    template_name = "items/object_confirm_delete.html"


class StdProductsList(TemplateView):
    template_name = 'items/std_products_list.html'


class StdProductCreate(FormView):
    template_name = 'items/std_products/std_product_form.html'
    success_url = reverse_lazy('product_list')

    def dispatch(self, request, *args, **kwargs):
        product = STD_PRODUCTS[int(self.kwargs['product_num'])]
        self.form_class = product['form_class']
        return super(StdProductCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.create_product()
        return super(StdProductCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(StdProductCreate, self).get_context_data(**kwargs)
        product = STD_PRODUCTS[int(self.kwargs['product_num'])]
        context['header'] = product['header']
        context['form_type'] = product['form_type']
        return context


@login_required(login_url='/login/')
def create_ptz_shifter(request):
    create_ptz_shifter_()
    return redirect('product_list')
