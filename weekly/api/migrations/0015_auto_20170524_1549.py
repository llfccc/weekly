# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-24 07:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0014_auto_20170524_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saletarget',
            name='sale_target_owner_id',
        ),
        migrations.AddField(
            model_name='saletarget',
            name='sale_target_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u76ee\u6807\u6240\u5c5e\u4eba'),
            preserve_default=False,
        ),
    ]
