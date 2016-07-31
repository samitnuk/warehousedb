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

    notes = models.TextField(
        blank=True,
        verbose_name="Примітка",
    )

    @property
    def current_total(self):
        return self.quantity.aggregate(models.Sum('additional_quantity'))

    def __str__(self):
        total = self.current_total['additional_quantity__sum']
        if self.part_number:
            return '%s (%s) - %s шт.' % (self.title,
                                         self.part_number,
                                         total)
        return '%s - %s шт.' % (self.title, total)


class ItemChange(models.Model):

    class Meta(object):
        verbose_name = "Зміна кількості"
        verbose_name_plural = "Зміни кількості"

    additional_quantity = models.IntegerField(
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

    def __str__(self):
        return '%s / (%s) - %d' % (self.item,
                                   self.changed_at.strftime('%Y-%m-%d'),
                                   self.additional_quantity)
