# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zhidao', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='Time',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='Time',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='information',
            field=models.TextField(null=True, blank=True),
        ),
    ]
