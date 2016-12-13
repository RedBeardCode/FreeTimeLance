# coding=utf-8
"""
DB Models for the application
"""
from json import dumps

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.utils.timezone import timedelta
from invitations.models import Invitation
from invitations.signals import invite_accepted


def user_accepted_invitation(sender, **kwargs):
    pass


class CustomerInvitation(Invitation):
    customer = models.ForeignKey('Customer', blank=True, null=True)


invite_accepted.connect(user_accepted_invitation)


def after_costumer_saved(sender, instance, created, *args, **kwargs):
    """
    Post saved function for the Costumer model, to create for each costumer a
    user group
    """
    if created:
        Group.objects.get_or_create(name=instance.get_group_name())


@python_2_unicode_compatible
class Customer(models.Model):
    """
    Customer who ordered the project
    """
    name = models.CharField('Name of the customer', max_length=250)

    def __str__(self):
        return self.name

    def get_group_name(self):
        """
        Name of the user group
        """
        return self.name

    def get_group(self):
        """
        Returns the user group for the customer
        """
        return Group.objects.get_or_create(name=self.get_group_name())


post_save.connect(after_costumer_saved, sender=Customer)


def after_project_saved(sender, instance, created, *args, **kwargs):
    """
    Post save function to save the costumer user group as foreign key in the
    project. It is imported to enable filtering of the querysets.
    """
    if created:
        instance.group = instance.customer.get_group()[0]
        instance.save()


@python_2_unicode_compatible
class Project(models.Model):
    """
    Project for which you get a order
    """
    name = models.CharField('Name of the project', max_length=250)
    customer = models.ForeignKey('Customer')
    description = models.TextField('Description of the target of the project')
    start_date = models.DateField('Start date')
    death_line = models.DateField('Death line')
    workload = models.DurationField('Submitted number of working hours')
    repository = models.URLField('Url of the repository')
    group = models.ForeignKey('auth.Group', blank=True, null=True)

    def __str__(self):
        return "Project: " + self.name

    def get_group(self):
        """
        Returns to user group of the customer of the project
        """
        return self.group

    def get_durations_dump(self):
        """
        Creates a json list for the nv3d chart with the activities of the
        project
        """
        times = list()
        sum_time = timedelta()
        for activity in self.activity_set.all().order_by('start_time'):
            times.append(
                {'label': activity.remarks,
                 'value': activity.duration().total_seconds() / 3600.0})
            sum_time += activity.duration()
        time_left = self.workload - sum_time
        times.append({'label': 'Restzeit',
                      'value': time_left.total_seconds() / 3600.0})
        return dumps(times)


post_save.connect(after_project_saved, sender=Project)


@python_2_unicode_compatible
class Activity(models.Model):
    """
    Single activity of your daily work
    """
    hamster_id = models.IntegerField('Id of hamster activity', unique=True, blank=True, null=True)
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time')
    project = models.ForeignKey('Project')
    remarks = models.TextField('Remarks for the done work', null=True)

    def duration(self):
        """
        Returns the calculated duration as timedelta
        """
        return self.end_time - self.start_time

    def __str__(self):
        return self.project.name + ": " + self.remarks[:10]
