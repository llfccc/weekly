# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-24 07:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20170524_1412'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weeksummary',
            options={'permissions': (('analysi_weekly_summary', '\u4e3b\u7ba1:\u67e5\u770b\u5458\u5de5\u6bcf\u5468\u5468\u62a5\u5206\u6790'),)},
        ),
    ]