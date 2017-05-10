# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-09 06:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20170509_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chinese_name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='\u4e2d\u6587\u540d'),
        ),
        migrations.AddField(
            model_name='user',
            name='department_id',
            field=models.IntegerField(default=1, verbose_name='\u90e8\u95e8id'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='position_id',
            field=models.IntegerField(default=1, verbose_name='\u804c\u4f4did'),
            preserve_default=False,
        ),
    ]