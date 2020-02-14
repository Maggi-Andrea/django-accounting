from django.views import generic
from django.urls import reverse

from accounting.apps.books.mixins import (
    RestrictToSelectedOrganizationQuerySetMixin,
    AutoSetSelectedOrganizationMixin)

from .models import Client, Employee, FiscalProfile
from .forms import ClientForm, EmployeeForm, FiscalProfileForm


class FiscalProfileCreateView(generic.CreateView):

  template_name = "accounting/people/fiscalprofile_edit.html"

  model = FiscalProfile

  form_class = FiscalProfileForm

  def form_valid(self, form):
    profile = form.save(commit=False)
    profile.user = self.request.user
    profile.save()
    return super().form_valid(form)

class FiscalProfileDetailView(generic.DetailView):

  template_name = "accounting/people/fiscalprofile_detail.html"

  model = FiscalProfile

  def get(self, request, *args, **kwargs):
    try:
      self.get_object()
    except Exception as e:
      FiscalProfile(request.user, fiscal_id = request.user.username).save()
    return super().get(request, *args, **kwargs)

class FiscalProfileEditView(generic.UpdateView):

  template_name = "accounting/people/fiscalprofile_edit.html"

  model = FiscalProfile

  form_class = FiscalProfileForm

class ClientListView(RestrictToSelectedOrganizationQuerySetMixin,
                     generic.ListView):
    template_name = "people/client/list.html"
    model = Client
    context_object_name = "clients"

class ClientCreateView(AutoSetSelectedOrganizationMixin,
                       generic.CreateView):
    template_name = "people/client/create_or_update.html"
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse("people:client-list")


class ClientUpdateView(RestrictToSelectedOrganizationQuerySetMixin,
                       AutoSetSelectedOrganizationMixin,
                       generic.UpdateView):
    template_name = "people/client/create_or_update.html"
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse("people:client-list")


class ClientDetailView(RestrictToSelectedOrganizationQuerySetMixin,
                       generic.DetailView):
    template_name = "people/client/detail.html"
    model = Client
    context_object_name = "client"


class EmployeeListView(RestrictToSelectedOrganizationQuerySetMixin,
                       generic.ListView):
    template_name = "people/employee/list.html"
    model = Employee
    context_object_name = "employees"


class EmployeeCreateView(AutoSetSelectedOrganizationMixin,
                         generic.CreateView):
    template_name = "people/employee/create_or_update.html"
    model = Employee
    form_class = EmployeeForm

    def get_success_url(self):
        return reverse("people:employee-list")


class EmployeeUpdateView(RestrictToSelectedOrganizationQuerySetMixin,
                         AutoSetSelectedOrganizationMixin,
                         generic.UpdateView):
    template_name = "people/employee/create_or_update.html"
    model = Employee
    form_class = EmployeeForm

    def get_success_url(self):
        return reverse("people:employee-list")


class EmployeeDetailView(RestrictToSelectedOrganizationQuerySetMixin,
                         generic.DetailView):
    template_name = "people/employee/detail.html"
    model = Employee
    context_object_name = "employee"
