from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView

from ..models import Order
from ..forms import AddOrderForm


class OrderList(ListView):
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super(OrderList, self).get_queryset()
        if self.kwargs['status'] == 'sent':
            return queryset.filter(is_sent=True)
        elif self.kwargs['status'] == 'ready':
            return queryset.filter(is_ready=True, is_sent=False)
        else:
            return queryset.filter(is_ready=False)


class OrderCreate(FormView):
    template_name = 'items/order_form.html'
    form_class = AddOrderForm
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        form.create_order()
        return super(OrderCreate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')
    template_name = "items/object_confirm_delete.html"


class OrderDetail(DetailView):
    model = Order
    context_object_name = 'order'


def ready_confirmation(request, pk):

    order = Order.objects.filter(pk=pk).first()
    order.is_ready = True
    order.save()

    return redirect('order_list', status='ready')


def sent_confirmation(request, pk):

    order = Order.objects.filter(pk=pk).first()
    order.is_sent = True
    order.save()

    return redirect('order_list', status='sent')
