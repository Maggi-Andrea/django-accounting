from django.db.models.fields import FieldDoesNotExist
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

from .utils import organization_manager

class RestrictToSelectedOrganizationQuerySetMixin(object):
  """
  To restrict objects to the current selected organization
  """

  def get_restriction_filters(self):
    # check for the field
    meta = self.model._meta
    field = meta.get_field('organization')

    # build the restriction
    orga = organization_manager.get_selected_organization(self.request)
    return {field.name: orga.pk}

  def get_queryset(self):
    filters = self.get_restriction_filters()
    queryset = super().get_queryset()
    queryset = queryset.filter(**filters)
    return queryset

  def get(self, request, *args, **kwargs):
    orga = organization_manager.get_selected_organization(request)
    if orga is None:
      return HttpResponseRedirect(reverse('books:organization-selector'))
    return super().get(request, *args, **kwargs)


class RestrictToOrganizationFormRelationsMixin:
  """
  To restrict relations choices to the organization linked instances
  """
  relation_name = 'organization'

  def _restrict_fields_choices(self, model, organization, fields):
    for source in fields:
      field = model._meta.get_field(source)
      if not field.is_relation:
        # next field
        continue

      rel_model = field.related_model
      try:
        rel_model._meta.get_field(self.relation_name)
      except FieldDoesNotExist:
        # next field
        continue

      form_field = fields[source]
      form_field.widget.queryset = (form_field.widget.queryset
        .filter(**{self.relation_name: organization}))

  def restrict_fields_choices_to_organization(self, form, organization):
    assert organization is not None, "no organization to restrict to"
    model = form._meta.model
    self._restrict_fields_choices(model, organization, form.fields)


class SaleListQuerySetMixin:

  def get_queryset(self):
    queryset = super().get_queryset()
    queryset = (queryset
      .select_related('organization')
      .prefetch_related(
        'lines',
        'lines__tax_rate'))

    try:
      # to raise the exception
      self.model._meta.get_field('client')
      queryset = queryset.select_related('client')
    except FieldDoesNotExist:
      pass

    try:
      # to raise the exception
      self.model._meta.get_field('payments')
      queryset = queryset.prefetch_related('payments')
    except FieldDoesNotExist:
      pass

    return queryset


class AutoSetSelectedOrganizationMixin(object):

  def form_valid(self, form):
    obj = form.save(commit=False)
    orga = organization_manager.get_selected_organization(self.request)
    obj.organization = orga

    return super().form_valid(form)
  
class SaleLineCreateUpdateMixin(RestrictToOrganizationFormRelationsMixin):
  inlines_formset_pairs = None

  def get_context_data(self, **kwargs):
    assert self.inlines_formset_pairs is not None, "No formset class specified"
    context = super().get_context_data(**kwargs)
    orga = organization_manager.get_selected_organization(self.request)
    for formset_name, formset_class in self.inlines_formset_pairs:
      if self.request.POST:
        context[formset_name] = formset_class(
          data=self.request.POST,
          instance=self.object,
          organization=orga)
      else:
        context[formset_name] = formset_class(
          instance=self.object,
          organization=orga)
    return context

  def get_form(self, form_class=None):
    """Restrict the form relations to the current organization"""
    form = super().get_form(form_class)
    orga = organization_manager.get_selected_organization(self.request)
    self.restrict_fields_choices_to_organization(form, orga)
    return form

  def form_valid(self, form):
    context = self.get_context_data()
    for formset_name, _ in self.inlines_formset_pairs:
      line_formset = context[formset_name]
      if not line_formset.is_valid():
        return super().form_invalid(form)
    self.object = form.save()
    for formset_name, _ in self.inlines_formset_pairs:
      line_formset = context[formset_name]
      line_formset.instance = self.object
      line_formset.save()

    # update totals
    self.object.compute_totals()

    return super().form_valid(form)


class AbstractSaleDetailMixin(object):

  def get_queryset(self):
    queryset = super().get_queryset()
    queryset = queryset.select_related('organization')

    try:
      # to raise the exception
      self.model._meta.get_field('client')
      queryset = queryset.select_related('client')
    except FieldDoesNotExist:
      pass

    return queryset

  def get_object(self):
    # save some db queries by caching the fetched object
    if hasattr(self, '_object'):
      return getattr(self, '_object')

    obj = super().get_object()
    setattr(self, '_object', obj)
    return obj

  def get_context_data(self, **kwargs):
    ctx = super().get_context_data(**kwargs)
    obj = self.get_object()
    ctx["checklist"] = obj.full_check()
    ctx["lines"] = (obj.lines.all().select_related('tax_rate'))
    return ctx

class PaymentFormMixin(generic.edit.FormMixin):
  payment_form_class = None
  
  def get_form_class(self):
    assert self.payment_form_class is not None, "No formset class specified"
    return self.payment_form_class
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['payment_form'] = self.get_form()
    return context

  def post(self, request, *args, **kwargs):
    """
    Handles POST requests, instantiating a form instance with the passed
    POST variables and then checked for validity.
    """
    form = self.get_form(self.payment_form_class)
    if form.is_valid():
      return self.form_valid(form)
    else:
      return self.form_invalid(form)

  def form_valid(self, form):
    self.object = self.get_object()

    # save payment
    payment = form.save(commit=False)
    payment.content_object = self.object
    payment.save()
    return super().form_valid(form)
