# coding=utf-8
"""
Views of the project app
"""
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http.response import Http404, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic import FormView
from invitations.views import AcceptInvite

from project.models import Project, Activity, Customer, CustomerInvitation


def show_404(request):
    raise Http404()


class CustomerAcceptInvite(AcceptInvite):
    def post(self, *args, **kwargs):
        target = super(CustomerAcceptInvite, self).post(*args, **kwargs)
        accept_url = reverse_lazy('account_signup')
        if hasattr(target, 'url') and target.url == accept_url:
            invitation = self.get_object()
            target = redirect(target.url + invitation.key)
        return target


class CustomerSignUpView(FormView):
    template_name = 'registration/register.html'
    success_url = '/'
    form_class = UserCreationForm

    def form_valid(self, form):
        key = self.request.resolver_match.kwargs['key']
        invitation = get_object_or_404(CustomerInvitation, key=key)
        user = User.objects.create_user(form.cleaned_data['username'],
                                        invitation.email,
                                        form.cleaned_data['password1'])

        user.groups.add(invitation.customer.get_group()[0])
        user.save()
        login(self.request, user)
        return super(CustomerSignUpView, self).form_valid(form)


class ProjectListView(ListView):
    """
    List all projects of the logined customer. If the user is in the staff
    group all project will be shown
    """
    model = Project
    template_name = "project_list.html"

    def get_context_data(self, **kwargs):
        """
        Filters the list of projects to which the user is allowed to see
        """
        context = super(ProjectListView, self).get_context_data(**kwargs)
        projects = context['project_list']
        if not self.request.user.is_staff:
            project = projects.filter(group__in=self.request.user.groups.all())
            context['project_list'] = project
        return context


class ProjectView(UserPassesTestMixin, DetailView):
    """
    Overview for one project with pie chart and a table of all activities.
    The user has to be in the user group of the customer or staff to see
    the overview
    """
    template_name = "project_view.html"
    model = Project

    def test_func(self):
        """
        Tests if the user is in the right user group
        """
        try:
            if self.request.user.is_staff:
                return True
            return self.request.user in \
                self.get_object().get_group().user_set.all()
        except AttributeError:
            return False

    def get_context_data(self, **kwargs):
        """
        Adds the chart data to the context
        """
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['times'] = self.get_object().get_durations_dump()
        return context

    def post(self, request, *args, **kwargs):
        context = {}
        try:
            invitation = CustomerInvitation.create(request.POST['email'],
                                                   request.user)
            invitation.customer = self.get_object().customer
            invitation.save()
            invitation.send_invitation(request)
            context["form_message"] = "Successfully invited {0}".format(
                request.POST['email'])
            context["color"] = "#2aabd2"
        except IntegrityError:
            context["form_message"] = "{0} already invited".format(
                request.POST['email'])
            context["color"] = "#d58512"

        return JsonResponse(context)


class CreateProjectView(CreateView):
    """
    View to create a new project. Only for staff.
    """
    template_name = "project_edit_view.html"
    model = Project
    fields = ['name', 'customer', 'description', 'start_date', 'death_line',
              'workload', 'repository']
    success_url = reverse_lazy('project_list')


class UpdateProjectView(UpdateView):
    """
    View to update a project. Only for staff.
    """
    template_name = "project_edit_view.html"
    model = Project
    fields = ['name', 'customer', 'description', 'start_date', 'death_line',
              'workload', 'repository']
    success_url = reverse_lazy('project_list')


class DeleteProjectView(DeleteView):
    """
    View to delete a project. Only for staff.
    """
    model = Project
    template_name = "delete_base.html"
    success_url = reverse_lazy('project_list')


class ActivityView(UserPassesTestMixin, DetailView):
    """
    Display the activity details. The user has to be in the user group of the
    customer of the project or staff
    """
    model = Activity
    template_name = "activity_view.html"

    def test_func(self):
        """
        Tests if the user is in the right user group
        """
        try:
            if self.request.user.is_staff:
                return True
            return self.request.user in \
                self.get_object().project.get_group().user_set.all()
        except AttributeError:
            return False


class ActivityListView(ListView):
    """
    Lists all activities. Only for staff.
    """
    model = Activity
    template_name = "activity_list.html"


class CreateActivityView(CreateView):
    """
    View to create a new activity. Only for staff.
    """
    template_name = "activity_edit_view.html"
    model = Activity
    fields = ['start_time', 'end_time', 'project', 'remarks']
    success_url = reverse_lazy('activity_list')


class UpdateActivityView(UpdateView):
    """
    View to update a activity. Only for staff.
    """
    template_name = "activity_edit_view.html"
    model = Activity
    fields = ['start_time', 'end_time', 'project', 'remarks']
    success_url = reverse_lazy('activity_list')


class DeleteActivityView(DeleteView):
    """
    View to delete a activity. Only for staff.
    """
    model = Activity
    template_name = "delete_base.html"
    success_url = reverse_lazy('activity_list')


class CustomerListView(ListView):
    """
    List all customers. Only for staff
    """
    template_name = "customer_list.html"
    model = Customer


class CustomerView(DetailView):
    """
    Detail view of the customer information. Only for staff
    """
    template_name = "customer_view.html"
    model = Customer


class CreateCustomerView(CreateView):
    """
    View to create a new customer. Only for staff.
    """
    template_name = "customer_edit_view.html"
    model = Customer
    fields = ['name']
    success_url = reverse_lazy('customer_list')


class UpdateCustomerView(UpdateView):
    """
    View to update a customer. Only for staff.
    """
    template_name = "customer_edit_view.html"
    model = Customer
    fields = ['name']
    success_url = reverse_lazy('customer_list')


class DeleteCustomerView(DeleteView):
    """
    View to delete a customer. Only for staff.
    """
    model = Customer
    template_name = "delete_base.html"
    success_url = reverse_lazy('customer_list')
