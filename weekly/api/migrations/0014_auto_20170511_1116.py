# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-11 03:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20170511_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeksummary',
            name='end_time',
            field=models.DateField(verbose_name='\u7ed3\u675f\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='weeksummary',
            name='start_time',
            field=models.DateField(verbose_name='\u5f00\u59cb\u65f6\u95f4'),
        ),
    ]