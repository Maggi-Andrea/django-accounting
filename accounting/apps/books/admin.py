from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .utils import organization_manager
from . import models

class SaleInlineAdminMixin:
  
  organization_fileds = ()
  
  def get_formset(self, request, obj=None, **kwargs):
    formset = super().get_formset(request, obj, **kwargs)
    organization = organization_manager.get_selected_organization(request)
    form = formset.form
    for filed in self.organization_fileds:
      form_field = form.base_fields[filed]
      form_field.queryset = form_field.queryset.filter(organization=organization)
    return formset


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
  pass


@admin.register(models.TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
  pass


class PaymentInline(GenericTabularInline):
  model = models.Payment
  extra = 1


class EstimateLineInline(SaleInlineAdminMixin, admin.TabularInline):
  model = models.EstimateLine
  extra = 1
  organization_fileds = ['tax_rate',]


@admin.register(models.Estimate)
class EstimateAdmin(admin.ModelAdmin):
  inlines = (
    EstimateLineInline,
  )
  readonly_fields = (
    'total_incl_tax', 'total_excl_tax',
  )


class InvoiceLineInline(SaleInlineAdminMixin, admin.TabularInline):
  model = models.InvoiceLine
  extra = 0
  min_num = 1
  organization_fileds = ['tax_rate',]
  
  
class InvoiceContributionInline(SaleInlineAdminMixin, admin.TabularInline):
  model = models.InvoiceContribution
  extra = 0
  organization_fileds = ['tax_rate', 'contribution_rate']


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
  inlines = (
    InvoiceLineInline,
    InvoiceContributionInline,
    PaymentInline,
  )
  readonly_fields = (
    'total_incl_tax', 'total_excl_tax',
  )
  list_display = ('from_client', 'to_client', 'number', 'get_total_excl_tax')
  
  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(
      organization = organization_manager.get_selected_organization(request)
    )
  

class BillLineInline(SaleInlineAdminMixin, admin.TabularInline):
  model = models.BillLine
  extra = 1
  organization_fileds = ['tax_rate',]


@admin.register(models.Bill)
class BillAdmin(admin.ModelAdmin):
  inlines = (
    BillLineInline,
    PaymentInline,
  )
  readonly_fields = (
    'total_incl_tax', 'total_excl_tax',
  )


class ExpenseClaimLineInline(SaleInlineAdminMixin, admin.TabularInline):
  model = models.ExpenseClaimLine
  extra = 1
  organization_fileds = ['tax_rate',]


@admin.register(models.ExpenseClaim)
class ExpenseClaimAdmin(admin.ModelAdmin):
  inlines = (
    ExpenseClaimLineInline,
    PaymentInline,
  )
  readonly_fields = (
    'total_incl_tax', 'total_excl_tax',
  )


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
  pass
