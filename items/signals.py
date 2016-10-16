from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ItemChange, Order


@receiver(post_save, sender=Order)
def itemchange_auto_create(instance, **kwargs):

    order = instance
    order_quantity = order.quantity
    if order_quantity == int(order_quantity):
        order_quantity = int(order_quantity)

    if order.product.part_number:
        product_title = '{} - {}'.format(order.product.part_number,
                                         order.product.title)
    else:
        product_title = order.product.title

    for component in order.product.components:
        ItemChange.objects.create(
            additional_quantity=order.quantity * component.quantity * -1,
            item=component.item,
            notes='{} / {} шт. / {}'.format(product_title,
                                            order_quantity,
                                            order.customer),
            order=order)
