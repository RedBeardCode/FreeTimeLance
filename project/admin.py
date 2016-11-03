# coding=utf-8
"""
Configuration of the Admin interface
"""
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from project.models import Project, Customer, Activity


admin.site.register(Activity, ModelAdmin)
admin.site.register(Customer, ModelAdmin)
admin.site.register(Project, ModelAdmin)
