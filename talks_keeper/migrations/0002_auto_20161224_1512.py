# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-24 15:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talks_keeper', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='talk',
            options={'ordering': ['-date'], 'verbose_name': 'Розмова', 'verbose_name_plural': 'Розмови'},
        ),
        migrations.RenameField(
            model_name='talk',
            old_name='our_talk',
            new_name='is_our_talk',
        ),
    ]