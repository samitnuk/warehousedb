from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ..views import product


urlpatterns = [

    url(r'^list/',
        login_required(product.ProductList.as_view()),
        name='product_list'),

    url(r'^detail/(?P<pk>\d+)/',
        product.detail,
        name='product_detail'),

    url(r'^create/',
        product.create,
        name='product_create'),

    url(r'^delete/(?P<pk>\d+)/',
        product.delete,
        name='product_delete'),

    url(r'^create_std_cable/',
        product.create_std_cable,
        name='product_create_std_cable'),

    url(r'^create_tza_cable/',
        product.create_tza_cable,
        name='product_create_tza_cable'),

    url(r'^create_b_cable/',
        product.create_b_cable,
        name='product_create_b_cable'),

    url(r'^create_h_cable/',
        product.create_h_cable,
        name='product_create_h_cable'),
]
