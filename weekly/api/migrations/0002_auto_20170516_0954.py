# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-16 01:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devproject',
            name='creator',
        ),
        migrations.AddField(
            model_name='devproject',
            name='creator_id',
            field=models.IntegerField(null=True, verbose_name='\u521b\u5efa\u4eba'),
        ),
    ]
