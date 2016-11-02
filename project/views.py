from json import dumps

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from project.models import Project, Activity


class ProjectListView(ListView):
    model = Project
    template_name = "project_list.html"


class ProjectView(UserPassesTestMixin, DetailView):
    template_name = "project_view.html"
    model = Project

    def test_func(self):
        return self.request.user in self.get_object().get_group().user_set.all() or self.request.user.is_staff



    def get_context_data(self, **kwargs):

        context = super(ProjectView, self).get_context_data(**kwargs)
        context['times'] = self.get_object().get_durations_dump()
        return context


class ActivityView(DetailView):
    model = Activity
    template_name = "activity_view.html"


class ActivityListView(ListView):
    model = Activity
    template_name = "activity_list.html"