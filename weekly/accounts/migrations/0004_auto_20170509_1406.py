# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-09 06:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20170509_1404'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'permissions': (('view_department', '\u53ef\u4ee5\u67e5\u770b\u90e8\u95e8'),)},
        ),
    ]
