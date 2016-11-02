from json import dumps

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.utils.timezone import timedelta

# Create your models here.

def after_costumer_saved(sender, instance, created, *args, **kwargs):
    if created:
        group = Group.objects.get_or_create(name=instance.get_group_name());


@python_2_unicode_compatible
class Customer(models.Model):
    """
    Customer who ordered the project
    """
    name = models.CharField('Name of the customer', max_length=250)

    def __str__(self):
        return self.name


    def get_group_name(self):
        return self.name


    def get_group(self):
        return Group.objects.get_or_create(name=self.get_group_name())


post_save.connect(after_costumer_saved, sender=Customer)


def after_project_saved(sender, instance, created, *args, **kwargs):
    if created:
        group = Group.objects.get_or_create(name=instance.get_group_name())[0];



@python_2_unicode_compatible
class Project(models.Model):
    """
    Project for which you get a order
    """
    name = models.CharField('Name of the project', max_length=250)
    customer = models.ForeignKey('customer')
    description = models.TextField('Description of the target of the project')
    start_date = models.DateField('Start date')
    death_line = models.DateField('Death line')
    workload = models.DurationField('Submitted number of working hours')
    repository = models.URLField('Url of the repository')

    def __str__(self):
        return  "Project: " + self.name

    def get_group_name(self):
        return self.customer.name + "_" + self.name

    def get_group(self):
        return Group.objects.get_or_create(name=self.get_group_name())[0]

    def get_durations_dump(self):
        times = list() #{'label': 'test1',  'value': 10}, {'label':'Macht nix', 'value': 90}]
        sum_time = timedelta()
        for activity in self.activity_set.all().order_by('start_time'):
            times.append({'label': activity.remarks, 'value': activity.duration().total_seconds()/3600.0})
            sum_time += activity.duration()
        time_left = self.workload - sum_time
        times.append({'label': 'Restzeit', 'value': time_left.total_seconds()/3600.0})
        return dumps(times)

post_save.connect(after_project_saved, sender=Project)

@python_2_unicode_compatible
class Activity(models.Model):
    """
    Single activitiy of your daily work
    """
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time')
    project = models.ForeignKey('Project')
    remarks = models.TextField('Remarks for the done work')

    def duration(self):
        return self.end_time - self.start_time

    def __str__(self):
        return self.project.name + ": " + self.remarks[:10]