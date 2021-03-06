# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-13 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField(blank=True, null=True)),
                ('player_name', models.TextField(blank=True, null=True)),
                ('player_points', models.FloatField(blank=True, null=True)),
                ('accumulated', models.TextField(blank=True, null=True)),
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
            name='Pointstable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pointstable_id', models.IntegerField(blank=True, null=True)),
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
