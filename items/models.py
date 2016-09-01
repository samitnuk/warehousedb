from datetime import date

from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver


class Item(models.Model):
    """Item Model

       Describes separate item in warehouse.

    """

    class Meta(object):
        verbose_name = "Позиція на складі"
        verbose_name_plural = "Позиції на складі"

    title = models.CharField(max_length=256, blank=False,
                             verbose_name="Найменування")

    part_number = models.CharField(max_length=256, blank=True,
                                   verbose_name="Індекс")

    part_number2 = models.CharField(max_length=256, blank=True,
                                    verbose_name="Наш індекс")

    picture = models.ImageField(blank=True, null=True,
                                verbose_name="Зображення")

    category = models.ForeignKey('Category', blank=True, null=True,
                                 verbose_name="Категорія")

    notes = models.TextField(blank=True, verbose_name="Примітка")

    @property
    def current_total(self):
        total = self.quantity.aggregate(models.Sum('additional_quantity'))
        if total['additional_quantity__sum'] is not None:
            return total['additional_quantity__sum']
        return 0

    def __str__(self):
        if self.part_number:
            return '%s - %s' % (self.part_number, self.title,)
        return self.title


class ItemChange(models.Model):
    """ItemChange Model

       Describes each change in quantity of concrete item.

    """

    class Meta(object):
        verbose_name = "Зміна кількості"
        verbose_name_plural = "Зміни кількості"

    additional_quantity = models.FloatField(blank=False)

    item = models.ForeignKey('Item', related_name='quantity')

    changed_at = models.DateField(
        blank=False,
        default=date.today,
        verbose_name="Дата зміни",
    )

    notes = models.TextField(blank=True, verbose_name="Примітка")

    def __str__(self):
        a_q = self.additional_quantity
        if a_q == int(a_q):
            a_q = int(a_q)
        return '%s / %s / %s' % (self.item,
                                 self.changed_at.strftime('%Y-%m-%d'),
                                 a_q)


class Category(models.Model):
    """Category Model

       Describes category for items.

    """

    class Meta(object):
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    name = models.CharField(max_length=256, verbose_name="Назва")

    notes = models.TextField(blank=True, verbose_name="Примітка")

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product Model

       Instance of Product Model is set of instances of Component Model

    """

    class Meta(object):
        verbose_name = "Виріб"
        verbose_name_plural = "Вироби"

    title = models.CharField(max_length=256, blank=False,
                             verbose_name="Найменування")

    part_number = models.CharField(max_length=256, blank=True,
                                   verbose_name="Індекс")

    notes = models.TextField(blank=True, verbose_name="Примітка")

    @property
    def components(self):
        return self.component.all()

    def __str__(self):
        if self.part_number:
            return '%s - %s' % (self.part_number, self.title)
        return self.title


class Component(models.Model):
    """Component Model

       Describes component and quantity of this component
       in separate product.

    """

    class Meta(object):
        verbose_name = "Компонент"
        verbose_name_plural = "Компоненти"

    product = models.ForeignKey(Product, related_name='component')

    item = models.ForeignKey('Item')

    quantity = models.FloatField(blank=False)

    def __str__(self):
        return self.item


class Order(models.Model):
    """Order Model

       When instance of Order Model will be created,
       will be created related instances of ItemChange Model
       throught post_save signal.

    """

    class Meta(object):
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    customer = models.CharField(max_length=256, blank=False,
                                verbose_name="Замовник")

    order_date = models.DateField(blank=False, default=date.today,
                                  verbose_name="Дата зміни")

    product = models.ForeignKey('Product')

    quantity = models.FloatField(blank=False, verbose_name="Кількість")

    def __str__(self):
        return '%s / %s' % (self.order_date, self.customer)


@receiver(post_save, sender=Order)
def auto_create_item_change(instance, **kwargs):

    order = instance

    if order.products.part_number:
        product_title = '%s - %s' % (order.product.part_number,
                                     order.product.title)
    else:
        product_title = order.product.title

    for component in order.product.components:
        ItemChange.objects.create(
            additional_quantity=order.quantity * component.quantity * -1,
            item=component.item,
            notes='%s / %s шт. / %s' % (product_title,
                                        order.quantity,
                                        order.customer)
        )
