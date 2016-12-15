
from __future__ import unicode_literals

from django.db import models


class Activities(models.Model):
    name = models.TextField(blank=True, null=True)
    work = models.IntegerField(blank=True, null=True)
    activity_order = models.IntegerField(blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey('Categories')
    search_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activities'


class Categories(models.Model):
    name = models.TextField(blank=True, null=True)
    color_code = models.TextField(blank=True, null=True)
    category_order = models.IntegerField(blank=True, null=True)
    search_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class FactTags(models.Model):
    fact = models.ForeignKey('Facts', primary_key=True)
    tag = models.ForeignKey('Tags')

    class Meta:
        managed = False
        db_table = 'fact_tags'
        unique_together = ['fact_id', 'tag_id']


class Facts(models.Model):
    activity = models.ForeignKey('Activities')
    start_time = models.TextField(blank=True, null=True)
    end_time = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'facts'

    @property
    def tags(self):
        return [factag.tag for factag in self.facttags_set.all()]


class Tags(models.Model):
    name = models.TextField()
    autocomplete = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'tags'
