# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-16 18:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0020_auto_20170203_2058'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemchange',
            options={'ordering': ['-changed_at'], 'verbose_name': 'Позиція на складі (зміна кількості)', 'verbose_name_plural': 'Позиції на складі (зміна кількості)'},
        ),
        migrations.AlterModelOptions(
            name='materialchange',
            options={'ordering': ['-changed_at'], 'verbose_name': 'Матеріал (зміна кількості)', 'verbose_name_plural': 'Матеріали (зміна кількості)'},
        ),
        migrations.AlterModelOptions(
            name='toolchange',
            options={'ordering': ['-changed_at'], 'verbose_name': 'Інструмент (зміна кількості)', 'verbose_name_plural': 'Інструменти (зміна кількості)'},
        ),
    ]
