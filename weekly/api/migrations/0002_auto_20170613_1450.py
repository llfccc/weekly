# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-13 14:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='saletarget',
            unique_together=set([('natural_week', 'phase_name', 'sale_target_owner')]),
        ),
    ]
