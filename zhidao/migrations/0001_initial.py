# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='answer',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('Content', models.TextField()),
                ('is_best', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='question',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('Title', models.CharField(max_length=100)),
                ('KeyWords', models.CharField(max_length=100)),
                ('Description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('Name', models.CharField(unique=b'True', max_length=30)),
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('Gender', models.BooleanField(choices=[(b'F', b'Female'), (b'M', b'Male')])),
                ('Birthday', models.DateField()),
                ('Email', models.EmailField(max_length=100)),
                ('Passwords', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='UserID',
            field=models.ForeignKey(to='zhidao.user'),
        ),
        migrations.AddField(
            model_name='answer',
            name='QuestionID',
            field=models.ForeignKey(to='zhidao.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='UserID',
            field=models.ForeignKey(to='zhidao.user'),
        ),
    ]
