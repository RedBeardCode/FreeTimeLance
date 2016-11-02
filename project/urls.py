from django.conf.urls import url

from project.views import ProjectView, ProjectListView, ActivityView
from project.views import ActivityListView

urlpatterns = [
    url(r'^activity/(?P<pk>[0-9]+)/$', ActivityView.as_view(), name='activity_view'),
    url(r'^activity/$', ActivityListView.as_view(), name='activity_list'),
    url(r'^(?P<pk>[0-9]+)/$', ProjectView.as_view(), name='project_view'),
    url(r'^$', ProjectListView.as_view(), name='project_list'),
]

