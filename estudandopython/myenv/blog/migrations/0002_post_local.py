# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 23:25
from __future__ import unicode_literals

from django.db import migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='local',
            field=geoposition.fields.GeopositionField(default='N/A', max_length=42),
            preserve_default=False,
        ),
    ]
