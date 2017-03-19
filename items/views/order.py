from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from ..forms import AddOrderForm, AddSentNotesToOrderForm
from ..models import Order


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


@login_required(login_url='/login/')
def ready_confirmation(request, pk):

    order = Order.objects.filter(pk=pk).first()
    order.is_ready = True
    order.save()

    return redirect('order_list', status='ready')


class AddSentNotesToOrder(FormView):
    template_name = 'items/order_add_sent_notes_form.html'
    form_class = AddSentNotesToOrderForm
    success_url = reverse_lazy('order_list', kwargs={'status': 'sent'})

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        form.add_sent_notes(pk)
        return super(AddSentNotesToOrder, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddSentNotesToOrder, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['order'] = Order.objects.filter(pk=pk).first()
        return context


@login_required(login_url='/login/')
def paid_confirmation(request, pk):

    Order.objects.filter(pk=pk).update(is_paid=True)
    order = Order.objects.filter(pk=pk).first()
    if order.is_sent:
        return redirect('order_list', status='sent')
    elif order.is_ready:
        return redirect('order_list', status='ready')
    return redirect('order_list')
