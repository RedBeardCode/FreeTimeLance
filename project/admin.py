from django.contrib import admin
from django.contrib.admin import ModelAdmin

from project.models import Project, Customer, Activity
# Register your models here.


admin.site.register(Activity, ModelAdmin)
admin.site.register(Customer, ModelAdmin)
admin.site.register(Project, ModelAdmin)