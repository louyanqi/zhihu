# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-03 12:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_page', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='topics',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question', to='site_page.Topic'),
        ),
    ]
