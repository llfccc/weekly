# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-09 05:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='remark',
            new_name='department_remark',
        ),
        migrations.RenameField(
            model_name='devevent',
            old_name='remark',
            new_name='dev_event_remark',
        ),
        migrations.RenameField(
            model_name='deveventtype',
            old_name='remark',
            new_name='dev_event_type_remark',
        ),
        migrations.RenameField(
            model_name='devproject',
            old_name='remark',
            new_name='dev_project_remark',
        ),
        migrations.RenameField(
            model_name='saleactivetype',
            old_name='remark',
            new_name='sale_active_type_remark',
        ),
        migrations.RenameField(
            model_name='salecustomer',
            old_name='remark',
            new_name='sale_customer_remark',
        ),
        migrations.RenameField(
            model_name='saleevent',
            old_name='remark',
            new_name='sale_event_remark',
        ),
        migrations.RenameField(
            model_name='salephase',
            old_name='remark',
            new_name='sale_phase_remark',
        ),
        migrations.RenameField(
            model_name='saletarget',
            old_name='remark',
            new_name='sale_target_remark',
        ),
    ]
