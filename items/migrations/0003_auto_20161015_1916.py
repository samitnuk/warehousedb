# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-15 19:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_auto_20161015_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemchange',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.Order', verbose_name='Замовлення'),
        ),
    ]
