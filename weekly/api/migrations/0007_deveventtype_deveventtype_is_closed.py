# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-18 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_devproject_project_is_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='deveventtype',
            name='devEventType_is_closed',
            field=models.BooleanField(default=False, verbose_name='true\u4ee3\u8868\u5173\u95ed'),
        ),
    ]
