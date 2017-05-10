# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-10 01:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20170510_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='devevent',
            name='event_date',
            field=models.DateField(default='2015-1-1', verbose_name='\u4e8b\u4ef6\u65e5\u671f'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='devevent',
            name='end_time',
            field=models.TimeField(verbose_name='\u4e8b\u4ef6\u7ed3\u675f\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='devevent',
            name='start_time',
            field=models.TimeField(verbose_name='\u4e8b\u4ef6\u5f00\u59cb\u65f6\u95f4'),
        ),
    ]