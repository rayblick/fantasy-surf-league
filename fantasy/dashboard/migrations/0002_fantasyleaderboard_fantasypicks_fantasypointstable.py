# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-14 03:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fantasyleaderboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField(blank=True, null=True)),
                ('player_name', models.TextField(blank=True, null=True)),
                ('player_points', models.FloatField(blank=True, null=True)),
                ('accumulated', models.FloatField(blank=True, null=True)),
                ('eventrank', models.IntegerField(blank=True, null=True)),
                ('tourrank', models.IntegerField(blank=True, null=True)),
                ('rankchange', models.IntegerField(blank=True, null=True)),
                ('requiredpoints', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'FantasyLeaderBoard',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Fantasypicks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_name', models.TextField(blank=True, null=True)),
                ('event_name', models.TextField(blank=True, null=True)),
                ('round_start_id', models.IntegerField(blank=True, null=True)),
                ('surfer_name', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'FantasyPicks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Fantasypointstable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points_id', models.IntegerField(blank=True, null=True)),
                ('event_id', models.IntegerField(blank=True, null=True)),
                ('round_id', models.IntegerField(blank=True, null=True)),
                ('bonusflag', models.TextField(blank=True, null=True)),
                ('surfer_name', models.TextField(blank=True, null=True)),
                ('total', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'FantasyPointsTable',
                'managed': False,
            },
        ),
    ]
