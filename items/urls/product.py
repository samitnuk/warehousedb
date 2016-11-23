from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ..views import product


urlpatterns = [

    url(r'^list/',
        login_required(product.ProductList.as_view()),
        name='product_list'),

    url(r'^detail/(?P<pk>\d+)/',
        login_required(product.ProductDetail.as_view()),
        name='product_detail'),

    url(r'^create/',
        login_required(product.ProductCreate.as_view()),
        name='product_create'),

    url(r'^delete/(?P<pk>\d+)/',
        login_required(product.ProductDelete.as_view()),
        name='product_delete'),

    url(r'^std_products_list/',
        login_required(product.StdProductsList.as_view()),
        name='std_products_list'),

    url(r'^create_std_product/(?P<product_num>\d+)/',
        login_required(product.StdProductCreate.as_view()),
        name='create_std_product'),
]
