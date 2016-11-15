#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Helper function for testing the project app
"""
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User
from ..models import Customer, Activity, Project


def create_customers():
    """
    Create sample customers for unit tests
    """
    for i in range(5):
        customer, _ = Customer.objects.get_or_create(name="Customer_{0}".format(i))
        user, _ = User.objects.get_or_create(username=customer.name)
        user.set_password('Start123')
        user.save()


def create_projects():
    """
    Create sample projects for unit tests
    """
    for customer in Customer.objects.all():
        for i in range(10):
            project, _ = Project.objects.get_or_create(name="{0}_Project_{1}".format(customer.name, i),
                                                       customer=customer,
                                                       description="Test project {0}".format(i),
                                                       start_date=now(),
                                                       death_line=now() + timedelta(days=(i + 2) * 10),
                                                       workload=timedelta(hours=80),
                                                       repository="http://localhost/"
                                                       )
            group = project.get_group()
            user = User.objects.get(username=customer.name)
            user.groups.add(group)


def create_activities():
    """
    Creates sample activities for unit tests
    """
    for project in Project.objects.all():
        for i in range(10):
            _ = Activity.objects.get_or_create(start_time=now(),
                                               end_time=now() + timedelta(hours=i * 1),
                                               project=project,
                                               remarks="Test activity {0}".format(i)
                                               )


def create_test_data():
    """
    Creates sample data(customers, activities and projects) for unit test
    """

    create_customers()
    create_projects()
    create_activities()

