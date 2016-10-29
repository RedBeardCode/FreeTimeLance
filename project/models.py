from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    """
    Customer who ordered the project
    """
    name = models.CharField('Name of the customer', max_length=250)

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

class Activity(models.Model):
    """
    Single activitiy of your daily work
    """
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time')
    project = models.ForeignKey('Project')
    remarks = models.TextField('Remarks for the done work')

    def duration(self):
        return end_time - start_time