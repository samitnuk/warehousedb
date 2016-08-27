from datetime import date

from django.db import models


class Item(models.Model):
    """Item Model"""

    class Meta(object):
        verbose_name = "Компонент"
        verbose_name_plural = "Компоненти"

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name="Найменування",
    )

    part_number = models.CharField(
        max_length=256,
        blank=True,
        verbose_name="Індекс",
    )

    part_number2 = models.CharField(
        max_length=256,
        blank=True,
        verbose_name="Наш індекс",
    )

    picture = models.ImageField(
        blank=True,
        null=True,
        verbose_name="Зображення",
    )

    category = models.ForeignKey(
        'Category',
        blank=True,
        null=True,
        verbose_name="Категорія",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Примітка",
    )

    @property
    def current_total(self):
        total = self.quantity.aggregate(models.Sum('additional_quantity'))
        if total['additional_quantity__sum'] is not None:
            return total['additional_quantity__sum']
        return 0

    def __str__(self):
        c_t = self.current_total
        if c_t == int(c_t):
            c_t = int(c_t)
        if self.part_number:
            return '%s (%s) - %s шт.' % (self.title,
                                         self.part_number,
                                         c_t)
        return '%s - %s шт.' % (self.title, c_t)


class ItemChange(models.Model):

    class Meta(object):
        verbose_name = "Зміна кількості"
        verbose_name_plural = "Зміни кількості"

    additional_quantity = models.FloatField(
        blank=False,
    )

    item = models.ForeignKey(
        'Item',
        related_name='quantity',
    )

    changed_at = models.DateField(
        blank=False,
        default=date.today,
        verbose_name="Дата зміни",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Примітка",
    )

    def __str__(self):
        a_q = self.additional_quantity
        if a_q == int(a_q):
            a_q = int(a_q)
        return '%s / %s / %s' % (self.item,
                                 self.changed_at.strftime('%Y-%m-%d'),
                                 a_q)


class Category(models.Model):

    class Meta(object):
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    name = models.CharField(
        max_length=256,
        verbose_name="Назва",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Примітка",
    )

    def __str__(self):
        return self.name


class Product (models.Model):
    """Product Model
       
       product = set of components

       Instance of Product model is
       set of instances of Component model

    """

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name="Найменування",
    )

    part_number = models.CharField(
        max_length=256,
        blank=True,
        verbose_name="Індекс",
    )

    created_at = models.DateField(
        blank=False,
        default=date.today,
        verbose_name="Дата створення",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Примітка",
    )

    @property
    def components(self):
        return self.component.all()


class Component(models.Model):

    product = models.ForeignKey(
        Product,
        related_name='component',
    )

    item = models.ForeignKey(
        'Item',
    )

    quantity = models.FloatField(
        blank=False,
    )