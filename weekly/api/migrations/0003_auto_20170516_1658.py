# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-16 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170516_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devevent',
            name='down_reporter_ids',
            field=models.CharField(max_length=64, verbose_name='\u4e0b\u6e38\u4ea4\u63a5\u4eba'),
        ),
    ]