# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-13 10:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20170913_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='code',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opportunity',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='usercode',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 9, 13, 10, 54, 53, 885000, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usercode',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='userkeyword',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userkeyword',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='useropportunity',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='useropportunity',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
