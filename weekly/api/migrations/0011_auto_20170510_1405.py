# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-10 06:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20170510_0958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devevent',
            old_name='owner_id',
            new_name='dev_event_owner_id',
        ),
        migrations.RenameField(
            model_name='devevent',
            old_name='project_id',
            new_name='dev_event_project_id',
        ),
        migrations.RenameField(
            model_name='devevent',
            old_name='event_type_id',
            new_name='dev_event_type_id',
        ),
    ]