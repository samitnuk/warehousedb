from datetime import date

from django.db import models


class Base(models.Model):
    """Base abstract model

    Used as base for some other models.

    """

    title = models.CharField(max_length=256, verbose_name="Найменування")

    notes = models.TextField(blank=True, verbose_name="Примітка")

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class BaseChange(models.Model):
    """BaseChange abstract model

    Used as base for some other models that relate to quantity change.

    """

    additional_quantity = models.FloatField(blank=False)

    changed_at = models.DateField(blank=False,
                                  default=date.today,
                                  verbose_name="Дата зміни")

    notes = models.TextField(blank=True, verbose_name="Примітка")

    class Meta:
        abstract = True
