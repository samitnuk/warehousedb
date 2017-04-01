from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    Component, Item, ItemChange, MaterialChange, Order, ToolChange)


@receiver(post_save, sender=Order)
def itemchange_auto_create(instance, **kwargs):

    order = instance
    if order.is_ready:
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
def after_itemchange_created_or_updated(instance, **kwargs):

    itemchange = instance

    # Instance of MaterialChange Model should be created if
    # additional_quantity is positive and material selected
    if itemchange.additional_quantity > 0 and itemchange.material and \
            itemchange.item.rate:

        a_q = itemchange.additional_quantity
        if a_q == int(a_q):
            a_q = int(a_q)

        MaterialChange.objects.update_or_create(
            additional_quantity=(a_q * itemchange.item.rate * -1),
            material=itemchange.material,
            itemchange=itemchange,
            notes="{} {} / {} шт.".format(
                itemchange.item.title,
                itemchange.item.part_number,
                a_q),
            defaults={'itemchange': itemchange},
        )

    # Clean cache
    key = 'item_{}_current_total'.format(itemchange.item.id)
    cache.delete(key)


@receiver(post_save, sender=Item)
def after_item_created_or_updated(instance, **kwargs):

    item = instance

    components = Component.objects.filter(item=item)
    for component in components:
        product_id = component.product_id
        cache.delete('product_{}_weight'.format(product_id))
        cache.delete('product_{}_weight_is_correct'.format(product_id))


@receiver(post_save, sender=MaterialChange)
def after_materialchange_created_or_updated(instance, **kwargs):
    # Clean cache
    key = 'material_{}_current_total'.format(instance.material.id)
    cache.delete(key)


@receiver(post_save, sender=ToolChange)
def after_materialchange_created_or_updated(instance, **kwargs):
    # Clean cache
    key = 'tool_{}_current_total'.format(instance.tool.id)
    cache.delete(key)
