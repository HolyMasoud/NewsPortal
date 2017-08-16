# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-11 11:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Captcha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CID', models.PositiveSmallIntegerField(default=0)),
                ('Cpic', models.CharField(max_length=50)),
                ('Cvalue', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=300)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventname', models.CharField(max_length=50)),
                ('eventdetail', models.CharField(max_length=100)),
                ('eventdate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NID', models.PositiveSmallIntegerField(default=0)),
                ('title', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=500)),
                ('image', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='NewsSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SID', models.PositiveSmallIntegerField(default=0)),
                ('Stitle', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('isadmin', models.BooleanField()),
                ('lastlogin', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='newssection',
            name='SAdmin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NEWS.Users'),
        ),
        migrations.AddField(
            model_name='news',
            name='sectionID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NEWS.NewsSection'),
        ),
        migrations.AddField(
            model_name='news',
            name='writerID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NEWS.Users'),
        ),
        migrations.AddField(
            model_name='logs',
            name='UID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NEWS.Users'),
        ),
        migrations.AddField(
            model_name='comments',
            name='NID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NEWS.News'),
        ),
    ]