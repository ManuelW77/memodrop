# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-13 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0005_auto_20171213_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='_area',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')], default=1, verbose_name='Area'),
        ),
    ]
