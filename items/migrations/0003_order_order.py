# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-19 17:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_auto_20161018_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order',
            field=models.BooleanField(default=False, verbose_name='Готовність замовлення'),
        ),
    ]
