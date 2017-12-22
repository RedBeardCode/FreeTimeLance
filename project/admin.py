# -*- coding: utf-8 -*-
"""
Configuration of the Admin interface
"""
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from project.models import FreelanceProject, Customer, Activity
from project.models import EmployeeProject

admin.site.register(Activity, ModelAdmin)
admin.site.register(Customer, ModelAdmin)
admin.site.register(FreelanceProject, ModelAdmin)
admin.site.register(EmployeeProject, ModelAdmin)
