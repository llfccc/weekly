# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-26 05:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20170526_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deveventtype',
            name='devEventType_is_closed',
        ),
        migrations.RemoveField(
            model_name='devproject',
            name='status',
        ),
        migrations.AddField(
            model_name='deveventtype',
            name='closed_status',
            field=models.IntegerField(choices=[(0, '\u542f\u7528'), (1, '\u7981\u7528')], default=0, verbose_name='1\u4ee3\u8868\u5173\u95ed'),
        ),
        migrations.AddField(
            model_name='saleactivetype',
            name='closed_status',
            field=models.IntegerField(choices=[(0, '\u542f\u7528'), (1, '\u7981\u7528')], default=0, verbose_name='1\u4ee3\u8868\u5173\u95ed'),
        ),
        migrations.AddField(
            model_name='salecustomer',
            name='closed_status',
            field=models.IntegerField(choices=[(0, '\u542f\u7528'), (1, '\u7981\u7528')], default=0, verbose_name='1\u4ee3\u8868\u5173\u95ed'),
        ),
        migrations.AddField(
            model_name='salephase',
            name='closed_status',
            field=models.IntegerField(choices=[(0, '\u542f\u7528'), (1, '\u7981\u7528')], default=0, verbose_name='1\u4ee3\u8868\u5173\u95ed'),
        ),
    ]
