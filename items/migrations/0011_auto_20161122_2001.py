# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0010_auto_20161122_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='rate',
            field=models.FloatField(default=0, verbose_name='Норма витрати, м'),
        ),
        migrations.AlterField(
            model_name='item',
            name='weight',
            field=models.FloatField(default=0, verbose_name='Вага, кг'),
        ),
    ]
