from json import dumps
from django.shortcuts import render
from django.views.generic import DetailView
# Create your views here.
from project.models import Project


class ProjectView(DetailView):
    template_name = "project_view.html"
    model = Project

    def get_context_data(self, **kwargs):

        context = super(ProjectView, self).get_context_data(**kwargs)
        times = [{'label': 'test1',  'value': 10}, {'label':'Macht nix', 'value': 90}]
        context['times'] = dumps(times)
        return context