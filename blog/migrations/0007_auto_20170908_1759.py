# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 17:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20170908_1539'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=80)),
            ],
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Code'),
        ),
        migrations.AlterUniqueTogether(
            name='usercode',
            unique_together=set([]),
        ),
    ]
