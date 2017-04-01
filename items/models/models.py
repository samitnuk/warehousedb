from datetime import date

from django.core.cache import cache
from django.db import models
from django.urls import reverse

from .base import Base, BaseChange


class Item(Base):
    """Item Model

    Describes separate item in warehouse.

    """

    part_number = models.CharField(max_length=256, blank=True,
                                   verbose_name="Індекс")

    part_number2 = models.CharField(max_length=256, blank=True,
                                    verbose_name="Наш індекс")

    picture = models.ImageField(blank=True, null=True,
                                verbose_name="Зображення")

    category = models.ForeignKey('Category',
                                 verbose_name="Категорія")

    rate = models.FloatField(default=0,
                             verbose_name="Норма витрати, м")

    weight = models.FloatField(default=0,
                               verbose_name="Вага, кг")

    critical_qty = models.FloatField(default=0,
                                     verbose_name="Критична кількість")

    class Meta:
        verbose_name = "Позиція на складі"
        verbose_name_plural = "Позиції на складі"
        ordering = ['category', 'title', 'part_number']

    def __str__(self):
        if self.part_number:
            return '{} - {}'.format(self.part_number, self.title,)
        return self.title

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})

    @property
    def current_total(self):
        key = 'item_{}_current_total'.format(self.id)
        cached_value = cache.get(key)
        if cached_value:
            return float(cached_value)
        total = self.i_quantity.aggregate(
            qty=models.Sum('additional_quantity')
        )
        if total['qty'] is not None:
            cache.set(key, str(total['qty']))
            return total['qty']
        cache.set(key, '0')
        return 0

    def changes(self):
        return self.i_quantity.all()


class Category(Base):
    """Category Model

    Describes category for items.

    """

    special = models.BooleanField(default=False,
                                  verbose_name="Спеціальна категорія")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ['title']


class Product(Base):
    """Product Model

    Instance of Product Model is set of instances of Component Model

    """

    part_number = models.CharField(max_length=256, blank=True,
                                   verbose_name="Індекс")

    class Meta:
        verbose_name = "Виріб"
        verbose_name_plural = "Вироби"
        ordering = ['-id']

    def __str__(self):
        if self.part_number:
            return '{} - {}'.format(self.part_number, self.title)
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    @property
    def components(self):
        key = 'product_{}_components'.format(self.id)
        cached_components = cache.get(key)
        if cached_components:
            return cached_components

        components = self.component.all()
        cache.set(key, components)
        return components

    @property
    def weight(self):
        key = 'product_{}_weight'.format(self.id)
        cached_weight = cache.get(key)
        if cached_weight:
            return float(cached_weight)

        weight = 0
        for component in self.components:
            weight += component.item.weight * component.quantity
        cache.set(key, str(weight))
        return weight

    @property
    def weight_is_correct(self):
        # return True if for all components indicated item.weight
        key = 'product_{}_weight_is_correct'.format(self.id)
        cached_value = cache.get(key)
        if cached_value:
            return True if cached_value == 'True' else False

        value = all([component.item.weight for component in self.components])
        if value:
            cache.set(key, 'True')
        else:
            cache.set(key, 'False')
        return value

    @property
    def related_to_any_order(self):
        return any(self.order.all())


class Component(models.Model):
    """Component Model

    Describes component and quantity of this component
    in separate product.

    """

    product = models.ForeignKey(Product, related_name='component')

    item = models.ForeignKey('Item')

    quantity = models.FloatField(blank=False)

    class Meta(object):
        verbose_name = "Компонент"
        verbose_name_plural = "Компоненти"

    def __str__(self):
        return '{}'.format(self.item)


class Order(models.Model):
    """Order Model

    When for instance of Order Model is_ready be set to True,
    be created related instances of ItemChange Model throught
    post_save signal.

    When instance of Order Model be deleted, be deleted related
    instances of ItemChange Model throught model manager.

    """

    customer = models.CharField(max_length=256, blank=False,
                                verbose_name="Замовник")

    order_date = models.DateField(blank=False, default=date.today,
                                  verbose_name="Дата зміни")

    product = models.ForeignKey('Product', related_name="order")

    quantity = models.FloatField(blank=False, verbose_name="Кількість")

    notes = models.TextField(blank=True, verbose_name="Примітка")

    is_paid = models.BooleanField(default=False,
                                  verbose_name="Замовлення оплачено")

    is_ready = models.BooleanField(default=False,
                                   verbose_name="Замовлення готове")

    is_sent = models.BooleanField(default=False,
                                  verbose_name="Замовлення відправлено")

    sent_notes = models.TextField(null=True,
                                  verbose_name="Дані про відправлення")

    class Meta(object):
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ['-order_date', '-id']

    def __str__(self):
        return '{} / {}'.format(self.order_date, self.customer)

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})


class Material(Base):
    """Material Model

    Describes separate material in warehouse.

    """

    critical_qty = models.FloatField(default=0,
                                     verbose_name="Критична кількість")

    class Meta:
        verbose_name = "Матеріал"
        verbose_name_plural = "Матеріали"
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('material_detail', kwargs={'pk': self.pk})

    @property
    def current_total(self):
        key = 'material_{}_current_total'.format(self.id)
        cached_value = cache.get(key)
        if cached_value:
            return float(cached_value)
        total = self.m_quantity.aggregate(
            qty=models.Sum('additional_quantity'))
        if total['qty'] is not None:
            cache.set(key, str(total['qty']))
            return total['qty']
        cache.set(key, '0')
        return 0

    def changes(self):
        return self.m_quantity.all()


class Tool(Base):
    """Tool Model

    Describes separate tool in warehouse.

    """

    critical_qty = models.FloatField(default=0,
                                     verbose_name="Критична кількість")

    class Meta(object):
        verbose_name = "Інструмент"
        verbose_name_plural = "Інструменти"
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('tool_detail', kwargs={'pk': self.pk})

    @property
    def current_total(self):
        key = 'tool_{}_current_total'.format(self.id)
        cached_value = cache.get(key)
        if cached_value:
            return float(cached_value)
        total = self.t_quantity.aggregate(
            qty=models.Sum('additional_quantity')
        )
        if total['qty'] is not None:
            cache.set(key, str(total['qty']))
            return total['qty']
        cache.set(key, '0')
        return 0

    def changes(self):
        return self.t_quantity.all()


class ItemChange(BaseChange):
    """ItemChange Model

    Describes each change in quantity of concrete item.

    """

    item = models.ForeignKey('Item', related_name='i_quantity')

    order = models.ForeignKey('Order', blank=True, null=True,
                              verbose_name="Замовлення")

    material = models.ForeignKey('Material', blank=True, null=True,
                                 verbose_name="Матеріал")

    class Meta:
        verbose_name = "Позиція на складі (зміна кількості)"
        verbose_name_plural = "Позиції на складі (зміна кількості)"
        ordering = ['-changed_at']

    def __str__(self):
        a_q = self.additional_quantity
        if a_q == int(a_q):
            a_q = int(a_q)
        return '{} / {} / {}'.format(self.item,
                                     self.changed_at.strftime('%Y-%m-%d'),
                                     a_q)

    def get_absolute_url(self):
        return reverse('itemchange_detail', kwargs={'pk': self.pk})


class MaterialChange(BaseChange):
    """ItemChange Model

    Describes each change in quantity of concrete material.

    When instance of ItemChange Model (with positive
    additional_quantity) be created, be created related instances
    of MaterialChange Model throught post_save signal.

    When instance of ItemChange Model be deleted, be deleted related
    instances of MaterialChange Model throught model manager.

    """

    material = models.ForeignKey('Material', related_name='m_quantity')

    itemchange = models.ForeignKey('ItemChange', blank=True, null=True,
                                   verbose_name="Зміна кількості")

    class Meta:
        verbose_name = "Матеріал (зміна кількості)"
        verbose_name_plural = "Матеріали (зміна кількості)"
        ordering = ['-changed_at']

    def __str__(self):
        if self.itemchange:
            return '{} / {} / {} / {}'.format(
                self.material,
                self.itemchange.item,
                self.changed_at.strftime('%Y-%m-%d'),
                self.additional_quantity)
        return '{} / {} / {}'.format(
            self.material,
            self.changed_at.strftime('%Y-%m-%d'),
            self.additional_quantity)

    def get_absolute_url(self):
        return reverse('materialchange_detail', kwargs={'pk': self.pk})


class ToolChange(BaseChange):
    """ToolChange Model

    Describes each change in quantity of concrete tool.

    """

    tool = models.ForeignKey('Tool', related_name='t_quantity')

    class Meta:
        verbose_name = "Інструмент (зміна кількості)"
        verbose_name_plural = "Інструменти (зміна кількості)"
        ordering = ['-changed_at']

    def __str__(self):
        return '{} / {} / {} шт.'.format(
            self.tool,
            self.changed_at.strftime('%Y-%m-%d'),
            int(self.additional_quantity))

    def get_absolute_url(self):
        return reverse('toolchange_detail', kwargs={'pk': self.pk})
