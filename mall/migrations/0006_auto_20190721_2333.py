# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-21 23:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0005_auto_20190721_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classify',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='mall.Classify'),
        ),
    ]
