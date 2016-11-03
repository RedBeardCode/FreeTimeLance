from json import dumps

from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from project.models import Project, Activity, Customer


class ProjectListView(ListView):
    model = Project
    template_name = "project_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        projects = context['project_list']
        if not self.request.user.is_staff:
            project = projects.filter(group__in=self.request.user.groups.all())
            context['project_list'] = project
        return context


class ProjectView(UserPassesTestMixin, DetailView):
    template_name = "project_view.html"
    model = Project

    def test_func(self):
        try:
            if self.request.user.is_staff:
                return True
            return self.request.user in self.get_object().get_group().user_set.all()
        except AttributeError:
            return False

    def get_context_data(self, **kwargs):

        context = super(ProjectView, self).get_context_data(**kwargs)
        context['times'] = self.get_object().get_durations_dump()
        return context


class CreateProjectView(CreateView):
    template_name = "project_edit_view.html"
    model=Project
    fields = ['name', 'customer', 'description', 'start_date', 'death_line', 'workload', 'repository']
    success_url = reverse_lazy('project_list')


class UpdateProjectView(UpdateView):
    template_name = "project_edit_view.html"
    model = Project
    fields = ['name', 'customer', 'description', 'start_date', 'death_line', 'workload', 'repository']
    success_url = reverse_lazy('project_list')


class DeleteProjectView(DeleteView):
    model=Project
    template_name = "delete_base.html"
    success_url = reverse_lazy('project_list')


class ActivityView(UserPassesTestMixin, DetailView):
    model = Activity
    template_name = "activity_view.html"

    def test_func(self):
        try:
            if self.request.user.is_staff:
                return True
            return self.request.user in self.get_object().project.get_group().user_set.all()
        except AttributeError:
            return False


class ActivityListView(ListView):
    model = Activity
    template_name = "activity_list.html"


class CreateActivityView(CreateView):
    template_name = "activity_edit_view.html"
    model = Activity
    fields = ['start_time', 'end_time', 'project', 'remarks']
    success_url = reverse_lazy('activity_list')

class UpdateActivityView(UpdateView):
    template_name = "activity_edit_view.html"
    model = Activity
    fields = ['start_time', 'end_time', 'project', 'remarks']
    success_url = reverse_lazy('activity_list')


class DeleteActivityView(DeleteView):
    model=Activity
    template_name = "delete_base.html"
    success_url = reverse_lazy('activity_list')


class CustomerListView(ListView):
    template_name = "customer_list.html"
    model = Customer


class CustomerView(DetailView):
    template_name = "customer_view.html"
    model = Customer


class CreateCustomerView(CreateView):
    template_name = "customer_edit_view.html"
    model = Customer
    fields = ['name']
    success_url = reverse_lazy('customer_list')


class UpdateCustomerView(UpdateView):
    template_name = "customer_edit_view.html"
    model = Customer
    fields = ['name']
    success_url = reverse_lazy('customer_list')


class DeleteCustomerView(DeleteView):
    model=Customer
    template_name = "delete_base.html"
    success_url = reverse_lazy('customer_list')
