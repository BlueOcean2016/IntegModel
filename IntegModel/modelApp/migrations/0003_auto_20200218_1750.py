# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-02-18 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelApp', '0002_auto_20200218_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='state_flag',
            field=models.CharField(choices=[('1', '\u5f00\u53d1\u4e2d'), ('2', '\u6d4b\u8bd5\u4e2d'), ('3', '\u5df2\u4e0a\u7ebf'), ('4', '\u5df2\u4e0b\u7ebf'), ('5', '\u5176\u4ed6')], default='1', max_length=16, verbose_name='\u8868\u72b6\u6001'),
        ),
    ]
