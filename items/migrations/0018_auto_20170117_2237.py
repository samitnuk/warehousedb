# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-17 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0017_auto_20161229_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='last_qty_update',
            field=models.DateField(blank=True, null=True, verbose_name='Дата останньої зміни к-сті'),
        ),
        migrations.AddField(
            model_name='item',
            name='previous_qty',
            field=models.FloatField(default=0, verbose_name='К-сть за попередній період'),
        ),
    ]
