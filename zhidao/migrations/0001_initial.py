# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('email', models.EmailField(unique=True, max_length=100)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('gender', models.IntegerField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('address', models.CharField(max_length=140, null=True, blank=True)),
                ('information', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='answer',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('Content', models.TextField()),
                ('is_best', models.BooleanField()),
                ('Time', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExQuestion',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('Description', models.TextField()),
                ('Time', models.DateField(auto_now_add=True)),
                ('AnswerID', models.ForeignKey(to='zhidao.answer')),
                ('UserID', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('Content', models.TextField()),
                ('UserID', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('is_view', models.BooleanField(default=False)),
                ('MessageType', models.IntegerField()),
                ('Time', models.DateField(auto_now_add=True)),
                ('AnswerID', models.ForeignKey(blank=True, to='zhidao.answer', null=True)),
                ('From', models.ForeignKey(related_name='From_id', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='question',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('Title', models.CharField(max_length=100)),
                ('KeyWords', models.CharField(max_length=100)),
                ('Description', models.TextField()),
                ('Time', models.DateField(auto_now_add=True)),
                ('UserID', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='QuestionID',
            field=models.ForeignKey(blank=True, to='zhidao.question', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='To',
            field=models.ForeignKey(related_name='To_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='QuestionID',
            field=models.ForeignKey(to='zhidao.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='UserID',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
