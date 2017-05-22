# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-22 09:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20170522_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='position_id',
        ),
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.Position'),
            preserve_default=False,
        ),
    ]
