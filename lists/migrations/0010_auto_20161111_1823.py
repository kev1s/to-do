# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-11 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0009_auto_20161111_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(default='', unique=True),
        ),
    ]
