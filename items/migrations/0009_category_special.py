# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-20 13:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0008_auto_20161101_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='special',
            field=models.BooleanField(default=False, verbose_name='Спеціальна категорія'),
        ),
    ]
