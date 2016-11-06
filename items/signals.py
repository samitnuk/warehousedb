from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ItemChange, MaterialChange, Order


@receiver(post_save, sender=Order)
def itemchange_auto_create(instance, **kwargs):

    order = instance
    if order.ready:
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
                order=order,
                material=None,
                notes='{} / {} шт. / {}'.format(
                    product_title,
                    order_quantity,
                    order.customer))


@receiver(post_save, sender=ItemChange)
def materialchange_auto_create(instance, **kwargs):

    itemchange = instance

    # instance of MaterialChange Model should be created if
    # additional_quantity is positive and material selected
    if itemchange.additional_quantity > 0 and itemchange.material:

        additional_quantity = itemchange.additional_quantity
        if additional_quantity == int(additional_quantity):
            additional_quantity = int(additional_quantity)

        MaterialChange.objects.create(
            additional_quantity=(
                itemchange.additional_quantity * itemchange.item.rate * -1),
            material=itemchange.material,
            itemchange=itemchange,
            notes="{} {} / {} шт.".format(
                itemchange.item.title,
                itemchange.item.part_number,
                additional_quantity))
