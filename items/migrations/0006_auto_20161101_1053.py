# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_auto_20161025_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemchange',
            name='additional_quantity',
            field=models.FloatField(verbose_name='Зміна кількості'),
        ),
        migrations.AlterField(
            model_name='materialchange',
            name='additional_quantity',
            field=models.FloatField(verbose_name='Зміна кількості'),
        ),
        migrations.AlterField(
            model_name='toolchange',
            name='additional_quantity',
            field=models.FloatField(verbose_name='Зміна кількості'),
        ),
    ]
