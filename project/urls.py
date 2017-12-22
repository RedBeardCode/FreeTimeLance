# -*- coding: utf-8 -*-
"""
Url routing of the project app
"""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required

from project.views import FreelanceProjectView, FreelanceProjectListView, DeleteFreelanceProjectView
from project.views import UpdateFreelanceProjectView, CreateFreelanceProjectView
from project.views import UpdateActivityView, CreateActivityView, ActivityView
from project.views import ActivityListView, DeleteActivityView
from project.views import CustomerView, CustomerListView, CreateCustomerView
from project.views import UpdateCustomerView, DeleteCustomerView

urlpatterns = [
    url(r'^activity/(?P<pk>[0-9]+)/$', login_required(ActivityView.as_view()),
        name='activity_view'),
    url(r'^activity/$',
        permission_required('is_staff')(ActivityListView.as_view()),
        name='activity_list'),
    url(r'^activity/create/$',
        permission_required('is_staff')(CreateActivityView.as_view()),
        name='create_activity_view'),
    url(r'^activity/update/(?P<pk>[0-9]+)/$',
        permission_required('is_staff')(UpdateActivityView.as_view()),
        name='update_activity_view'),
    url(r'^activity/delete/(?P<pk>[0-9]+)/$',
        permission_required('is_staff')(DeleteActivityView.as_view()),
        name='delete_activity_view'),
    url(r'^customer/(?P<pk>[0-9]+)/$', login_required(CustomerView.as_view()),
        name='customer_view'),
    url(r'^customer/$',
        permission_required('is_staff')(CustomerListView.as_view()),
        name='customer_list'),
    url(r'^customer/create/$',
        permission_required('is_staff')(CreateCustomerView.as_view()),
        name='create_customer_view'),
    url(r'^customer/update/(?P<pk>[0-9]+)/$',
        permission_required('is_staff')(UpdateCustomerView.as_view()),
        name='update_customer_view'),
    url(r'^customer/delete/(?P<pk>[0-9]+)/$',
        permission_required('is_staff')(DeleteCustomerView.as_view()),
        name='delete_customer_view'),
    url(r'^(?P<pk>[0-9]+)/$', login_required(FreelanceProjectView.as_view()),
        name='project_view'),
    url(r'^$', login_required(FreelanceProjectListView.as_view()), name='project_list'),
    url(r'^create/$',
        permission_required('is_staff')(CreateFreelanceProjectView.as_view()),
        name='create_project_view'),
    url(r'^update/(?P<pk>[0-9]+)/$',
        permission_required('is_staff')(UpdateFreelanceProjectView.as_view()),
        name='update_project_view'),
    url(r'^delete/(?P<pk>[0-9]+)/$',
        permission_required('is_staff')(DeleteFreelanceProjectView.as_view()),
        name='delete_project_view'),
]
