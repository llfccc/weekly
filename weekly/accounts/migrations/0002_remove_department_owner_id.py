# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-16 03:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='owner_id',
        ),
    ]