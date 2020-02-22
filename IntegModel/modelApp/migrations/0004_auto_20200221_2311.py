# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-02-21 15:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelApp', '0003_auto_20200218_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableDependency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.TextField(blank=True, default='', verbose_name='\u5907\u6ce8\u4f5c\u4e1a')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('after_table_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='after_table_id', to='modelApp.Table', verbose_name='\u540e\u7f6e\u8868')),
                ('before_table_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='before_table_id', to='modelApp.Table', verbose_name='\u524d\u7f6e\u8868')),
            ],
            options={
                'db_table': 'integ_table_dependency',
                'verbose_name': '\u8868\u5f15\u7528\u5173\u7cfb',
            },
        ),
        migrations.AlterUniqueTogether(
            name='tabledependency',
            unique_together=set([('before_table_id', 'after_table_id')]),
        ),
    ]