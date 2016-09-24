# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-24 07:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Назва')),
                ('notes', models.TextField(blank=True, verbose_name='Примітка')),
            ],
            options={
                'verbose_name_plural': 'Категорії',
                'verbose_name': 'Категорія',
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'Компоненти',
                'verbose_name': 'Компонент',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Найменування')),
                ('part_number', models.CharField(blank=True, max_length=256, verbose_name='Індекс')),
                ('part_number2', models.CharField(blank=True, max_length=256, verbose_name='Наш індекс')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Зображення')),
                ('notes', models.TextField(blank=True, verbose_name='Примітка')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.Category', verbose_name='Категорія')),
            ],
            options={
                'verbose_name_plural': 'Позиції на складі',
                'verbose_name': 'Позиція на складі',
            },
        ),
        migrations.CreateModel(
            name='ItemChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_quantity', models.FloatField()),
                ('changed_at', models.DateField(default=datetime.date.today, verbose_name='Дата зміни')),
                ('notes', models.TextField(blank=True, verbose_name='Примітка')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quantity', to='items.Item')),
            ],
            options={
                'verbose_name_plural': 'Зміни кількості',
                'verbose_name': 'Зміна кількості',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=256, verbose_name='Замовник')),
                ('order_date', models.DateField(default=datetime.date.today, verbose_name='Дата зміни')),
                ('quantity', models.FloatField(verbose_name='Кількість')),
            ],
            options={
                'verbose_name_plural': 'Замовлення',
                'verbose_name': 'Замовлення',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Найменування')),
                ('part_number', models.CharField(blank=True, max_length=256, verbose_name='Індекс')),
                ('notes', models.TextField(blank=True, verbose_name='Примітка')),
            ],
            options={
                'verbose_name_plural': 'Вироби',
                'verbose_name': 'Виріб',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.Product'),
        ),
        migrations.AddField(
            model_name='component',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.Item'),
        ),
        migrations.AddField(
            model_name='component',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='component', to='items.Product'),
        ),
    ]
