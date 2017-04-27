# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desidered behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class FantasyLeaderBoard(models.Model):
    id = models.IntegerField(primary_key=True)
    event_id = models.IntegerField(blank=True, null=True)
    sex = models.TextField(blank=True, null=True)
    player_name = models.TextField(blank=True, null=True)
    player_points = models.FloatField(blank=True, null=True)
    accumulated = models.FloatField(blank=True, null=True)
    eventrank = models.IntegerField(blank=True, null=True)
    tourrank = models.IntegerField(blank=True, null=True) 
    rankchange = models.IntegerField(blank=True, null=True)
    requiredpoints = models.FloatField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'FantasyLeaderBoard'


class FantasyPicks(models.Model):
    id = models.IntegerField(primary_key=True)
    player_name = models.TextField(blank=True, null=True)
    event_id = models.IntegerField(blank=True, null=True)
    event_name = models.TextField(blank=True, null=True)
    round_start_id = models.IntegerField(blank=True, null=True)
    sex = models.TextField(blank=True, null=True)
    surfer_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FantasyPicks'


class FantasyPointsTable(models.Model):
    id = models.IntegerField(primary_key=True)
    #points_id = models.IntegerField(blank=True, null=True)
    event_id = models.IntegerField(blank=True, null=True)
    round_id = models.IntegerField(blank=True, null=True)
    bonusflag = models.TextField(blank=True, null=True)
    sex = models.TextField(blank=True, null=True)
    surfer_name = models.TextField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FantasyPointsTable'
