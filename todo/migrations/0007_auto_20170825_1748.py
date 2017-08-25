# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 22:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_item_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
