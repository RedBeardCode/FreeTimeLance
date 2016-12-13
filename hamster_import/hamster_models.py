# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Activities(models.Model):
    #id = models.IntegerField(primary_key=True, blank=True, null=True)  # AutoField?
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    work = models.IntegerField(blank=True, null=True)
    activity_order = models.IntegerField(blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey('Categories')
    search_name = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'activities'


class Categories(models.Model):
    #id = models.IntegerField(primary_key=True, blank=True, null=True)  # AutoField?
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    color_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    category_order = models.IntegerField(blank=True, null=True)
    search_name = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'categories'


# class FactIndex(models.Model):
#     #id = models.TextField(blank=True, null=True)  # This field type is a guess.
#     name = models.TextField(blank=True, null=True)  # This field type is a guess.
#     category = models.TextField(blank=True, null=True)  # This field type is a guess.
#     description = models.TextField(blank=True, null=True)  # This field type is a guess.
#     tag = models.TextField(blank=True, null=True)  # This field type is a guess.
#
#     class Meta:
#         managed = False
#         db_table = 'fact_index'
#

# class FactIndexContent(models.Model):
#     docid = models.IntegerField(primary_key=True, blank=True, null=True)
#     c0id = models.TextField(blank=True, null=True)  # This field type is a guess.
#     c1name = models.TextField(blank=True, null=True)  # This field type is a guess.
#     c2category = models.TextField(blank=True, null=True)  # This field type is a guess.
#     c3description = models.TextField(blank=True, null=True)  # This field type is a guess.
#     c4tag = models.TextField(blank=True, null=True)  # This field type is a guess.
#
#     class Meta:
#         managed = False
#         db_table = 'fact_index_content'
#
#
# class FactIndexSegdir(models.Model):
#     level = models.IntegerField(primary_key=True, blank=True, null=True)
#     idx = models.IntegerField(primary_key=True, blank=True, null=True)
#     start_block = models.IntegerField(blank=True, null=True)
#     leaves_end_block = models.IntegerField(blank=True, null=True)
#     end_block = models.IntegerField(blank=True, null=True)
#     root = models.BinaryField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'fact_index_segdir'
#         unique_together = (('level', 'idx'),)
#
#
# class FactIndexSegments(models.Model):
#     blockid = models.IntegerField(primary_key=True, blank=True, null=True)
#     block = models.BinaryField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'fact_index_segments'


class FactTags(models.Model):
    fact = models.ForeignKey('Facts', primary_key=True)
    tag =models.ForeignKey('Tags')

    class Meta:
        managed = False
        db_table = 'fact_tags'
        unique_together = ['fact_id', 'tag_id']


class Facts(models.Model):
    #id = models.IntegerField(primary_key=True, blank=True, null=True)  # AutoField?
    activity = models.ForeignKey('Activities')
    start_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    end_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    description = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'facts'

    @property
    def tags(self):
        return [factag.tag for factag in self.facttags_set.all()]



class Tags(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.TextField()
    autocomplete = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'tags'


