# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-08 08:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170508_1617'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deveventtype',
            old_name='event_name',
            new_name='event_type_name',
        ),
    ]
