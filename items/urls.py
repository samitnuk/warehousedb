from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.main,
        name='main'),
    url(r'^category/(?P<pk>\d+)/', views.category,
        name='category'),
    url(r'^items_by_dates/', views.items_by_dates,
        name='items_by_dates'),
    url(r'^item_details/(?P<pk>\d+)/', views.item_details,
        name='item_details'),
    url(r'^item_change_details/(?P<pk>\d+)/', views.item_change_details,
        name='item_change_details'),
    url(r'^add_item_change/(?P<pk>\d+)/', views.add_item_change,
        name='add_item_change'),

    url(r'^create_new_product/', views.create_new_product,
        name='create_new_product'),
    url(r'^products/', views.products,
        name='products'),

    url(r'^login/', views.login,
        name='login'),
    url(r'^logout/', views.logout,
        name='logout'),
]