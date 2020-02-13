import logging
from decimal import Decimal as D

from django.views import generic
from django.urls import reverse, reverse_lazy

from django.db.models import Sum
from django.http import HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import (
  RestrictToSelectedOrganizationQuerySetMixin,
  SaleListQuerySetMixin,
  AutoSetSelectedOrganizationMixin,
  SaleLineCreateUpdateMixin,
  AbstractSaleDetailMixin,
  PaymentFormMixin)
from .models import (
  Organization,
  TaxRate,
  ContributionRate,
  Estimate,
  Invoice,
  Bill,
  ExpenseClaim,
  Payment)
from .forms import (
  OrganizationForm,
  TaxRateForm,
  ContributionRateForm,
  EstimateForm,
  EstimateLineFormSet,
  InvoiceForm,
  InvoiceLineFormSet,
  InvoiceContributionFormSet,
  BillForm,
  BillLineFormSet,
  ExpenseClaimForm,
  ExpenseClaimLineFormSet,
  PaymentForm)
from .utils import (
  organization_manager,
  EstimateNumberGenerator,
  InvoiceNumberGenerator,
  BillNumberGenerator,
  ExpenseClaimNumberGenerator)

logger = logging.getLogger(__name__)

class DashboardView(
    LoginRequiredMixin,
    generic.DetailView,
  ):
  template_name = "books/dashboard.html"
  model = Organization
  context_object_name = "organization"

  def get_object(self):
    return organization_manager.get_selected_organization(self.request)

  def get_context_data(self, **kwargs):
    ctx = super().get_context_data(**kwargs)
    organization = self.get_object()
    ctx['invoices'] = (organization.invoices.all()
      .select_related(
        'client',
        'organization')
      .prefetch_related(
        'lines',
        'lines__tax_rate',
        'payments')
      .distinct())
    ctx['bills'] = (organization.bills.all()
      .select_related(
        'client',
        'organization')
      .prefetch_related(
        'lines',
        'lines__tax_rate',
        'payments')
      .distinct())
    return ctx

  def get(self, request, *args, **kwargs):
    orga = organization_manager.get_selected_organization(self.request)
    if orga is None:
      return HttpResponseRedirect(reverse('books:organization-selector'))
    return super().get(request, *args, **kwargs)

#Organization

class OrganizationSelectorView(
    LoginRequiredMixin,
    generic.TemplateView,
  ):
  template_name = "books/organization/selector.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    orgas = organization_manager.get_user_organizations(user)
    cumulated_turnovers = (orgas
      .aggregate(sum=Sum('invoices__total_excl_tax'))["sum"]) or D('0')
    cumulated_debts = (orgas
      .aggregate(sum=Sum('bills__total_excl_tax'))["sum"]) or D('0')
    cumulated_profits = cumulated_turnovers - cumulated_debts

    context["organizations_count"] = orgas.count()
    context["organizations_cumulated_turnovers"] = cumulated_turnovers
    context["organizations_cumulated_profits"] = cumulated_profits
    context["organizations_cumulated_active_days"] = 0

    context["organizations"] = orgas
    context["last_invoices"] = Invoice.objects.all()[:10]

    return context


class OrganizationListView(generic.ListView):
  template_name = "books/organization/list.html"
  model = Organization
  context_object_name = "organizations"

  def get_queryset(self):
    # only current authenticated user organizations
    return organization_manager.get_user_organizations(self.request.user)


class OrganizationDetailView(generic.DetailView):
  template_name = "books/organization/detail.html"
  model = Organization
  context_object_name = "organization"

  def get_queryset(self):
    # only current authenticated user organizations
    return organization_manager.get_user_organizations(self.request.user)

  def get_context_data(self, **kwargs):
    ctx = super().get_context_data(**kwargs)
    organization = self.get_object()
    ctx['invoices'] = (organization.invoices.all()
      .select_related('client', 'organization')
      .prefetch_related('lines'))
    ctx['bills'] = (organization.bills.all()
      .select_related('client', 'organization')
      .prefetch_related('lines'))
    return ctx


class OrganizationCreateView(generic.CreateView):
  template_name = "books/organization/create_or_update.html"
  model = Organization
  form_class = OrganizationForm
  success_url = reverse_lazy("books:organization-list")

  def form_valid(self, form):
    obj = form.save(commit=False)
    obj.owner = self.request.user
    return super().form_valid(form)


class OrganizationUpdateView(generic.UpdateView):
  template_name = "books/organization/create_or_update.html"
  model = Organization
  form_class = OrganizationForm

  success_url = reverse_lazy("books:organization-list")

  def get_queryset(self):
    # only current authenticated user organizations
    return organization_manager.get_user_organizations(self.request.user)


class OrganizationSelectionView(generic.DetailView):
  model = Organization

  def get_queryset(self):
    # only current authenticated user organizations
    return organization_manager.get_user_organizations(self.request.user)

  def post(self, request, *args, **kwargs):
    orga = self.get_object()
    organization_manager.set_selected_organization(self.request, orga)
    return HttpResponseRedirect(reverse('books:dashboard'))

#Tax Rates

class TaxRateListView(RestrictToSelectedOrganizationQuerySetMixin, generic.ListView):
  template_name = "books/tax_rates/list.html"
  model = TaxRate
  context_object_name = "tax_rates"


class TaxRateCreateView(AutoSetSelectedOrganizationMixin, generic.CreateView):
  template_name = "books/tax_rates/create_or_update.html"
  model = TaxRate
  form_class = TaxRateForm
  success_url = reverse_lazy("books:tax_rate-list")


class TaxRateUpdateView(AutoSetSelectedOrganizationMixin, generic.UpdateView):
  template_name = "books/tax_rates/create_or_update.html"
  model = TaxRate
  form_class = TaxRateForm
  success_url = reverse_lazy("books:tax_rate-list")


class TaxRateDeleteView(generic.DeleteView):
  template_name = "accounting/_forms/delete.html"
  model = TaxRate
  success_url = reverse_lazy('books:tax_rate-list')

# Contribution Rates

class ContributionRateListView(
    RestrictToSelectedOrganizationQuerySetMixin,
    generic.ListView):

  template_name = "books/contribution_rates/list.html"
  model = ContributionRate
  context_object_name = "contribution_rates"

class ContributionRateCreateView(
    AutoSetSelectedOrganizationMixin,
    generic.CreateView):

  template_name = "books/contribution_rates/create_or_update.html"
  model = ContributionRate
  form_class = ContributionRateForm
  success_url = reverse_lazy("books:contribution_rate-list")

class ContributionRateUpdateView(
    AutoSetSelectedOrganizationMixin,
    generic.UpdateView):

  template_name = "books/contribution_rates/create_or_update.html"
  model = ContributionRate
  form_class = ContributionRateForm
  success_url = reverse_lazy("books:contribution_rate-list")



# Estimates

class EstimateListView(
    RestrictToSelectedOrganizationQuerySetMixin,
    SaleListQuerySetMixin,
    generic.ListView):

  template_name = "books/estimate/list.html"
  model = Estimate
  context_object_name = "estimates"


class EstimateCreateView(
    AutoSetSelectedOrganizationMixin,
    SaleLineCreateUpdateMixin,
    generic.CreateView):

  template_name = "books/_sale/create_or_update.html"
  model = Estimate
  form_class = EstimateForm
  inlines_formset_pairs = (('line_formset', EstimateLineFormSet),)
  success_url = reverse_lazy("books:estimate-list")

  def get_initial(self):
    initial = super().get_initial()

    orga = organization_manager.get_selected_organization(self.request)
    initial['number'] = EstimateNumberGenerator().next_number(orga)

    return initial


class EstimateUpdateView(
    AutoSetSelectedOrganizationMixin,
    SaleLineCreateUpdateMixin,
    generic.UpdateView):

  template_name = "books/_sale/create_or_update.html"
  model = Estimate
  form_class = EstimateForm
  inlines_formset_pairs = (('line_formset', EstimateLineFormSet),)
  success_url = reverse_lazy("books:estimate-list")


class EstimateDeleteView(generic.DeleteView):
  template_name = "accounting/_forms/delete.html"
  model = Estimate
  success_url = reverse_lazy('books:estimate-list')


class EstimateDetailView(
    AbstractSaleDetailMixin,
    generic.DetailView):
  template_name = "books/_sale/detail.html"
  model = Estimate
  context_object_name = "estimate"

  def get_success_url(self):
    return reverse('books:estimate-detail', args=[self.object.pk])


# Invoices

class InvoiceListView(
    RestrictToSelectedOrganizationQuerySetMixin,
    SaleListQuerySetMixin,
    generic.ListView):

  template_name = "books/invoice/list.html"
  model = Invoice
  context_object_name = "invoices"


class InvoiceCreateView(
    AutoSetSelectedOrganizationMixin,
    SaleLineCreateUpdateMixin,
    generic.CreateView):

  template_name = "books/_sale/create_or_update.html"
  model = Invoice
  form_class = InvoiceForm
  inlines_formset_pairs = (('line_formset', InvoiceLineFormSet),
               ('contribution_formset', InvoiceContributionFormSet))
  success_url = reverse_lazy("books:invoice-list")

  def get_initial(self):
    initial = super().get_initial()
    orga = organization_manager.get_selected_organization(self.request)
    initial['number'] = InvoiceNumberGenerator().next_number(orga)
    return initial


class InvoiceUpdateView(
    AutoSetSelectedOrganizationMixin,
    SaleLineCreateUpdateMixin,
    generic.UpdateView):

  template_name = "books/_sale/create_or_update.html"
  model = Invoice
  form_class = InvoiceForm
  inlines_formset_pairs = (('line_formset', InvoiceLineFormSet),
               ('contribution_formset', InvoiceContributionFormSet))
  success_url = reverse_lazy("books:invoice-list")


class InvoiceDeleteView(generic.DeleteView):
  template_name = "accounting/_forms/delete.html"
  model = Invoice
  success_url = reverse_lazy('books:invoice-list')


class InvoiceDetailView(
    PaymentFormMixin,
    AbstractSaleDetailMixin,
    generic.DetailView):

  template_name = "books/_sale/detail.html"
  model = Invoice
  context_object_name = "invoice"
  payment_form_class = PaymentForm

  def get_success_url(self):
    return reverse('books:invoice-detail', args=[self.object.pk])

# Bills

class BillListView(
    RestrictToSelectedOrganizationQuerySetMixin,
    SaleListQuerySetMixin,
    generic.ListView):

  template_name = "books/bill/list.html"
  model = Bill
  context_object_name = "bills"


class BillCreateView(
    AutoSetSelectedOrganizationMixin,
    SaleLineCreateUpdateMixin,
    generic.CreateView):

  template_name = "books/_sale/create_or_update.html"
  model = Bill
  form_class = BillForm
  inlines_formset_pairs = (('line_formset', BillLineFormSet),)
  success_url = reverse_lazy("books:bill-list")

  def get_initial(self):
    initial = super().get_initial()

    orga = organization_manager.get_selected_organization(self.request)
    initial['number'] = BillNumberGenerator().next_number(orga)

    return initial


class BillUpdateView(
    AutoSetSelectedOrganizationMixin,
    SaleLineCreateUpdateMixin,
    generic.UpdateView):

  template_name = "books/_sale/create_or_update.html"
  model = Bill
  form_class = BillForm
  inlines_formset_pairs = (('line_formset', BillLineFormSet),)
  success_url = reverse_lazy("books:bill-list")


class BillDeleteView(generic.DeleteView):
  template_name = "accounting/_forms/delete.html"
  model = Bill
  success_url = reverse_lazy('books:bill-list')


class BillDetailView(
    PaymentFormMixin,
    AbstractSaleDetailMixin,
    generic.DetailView):

  template_name = "books/_sale/detail.html"
  model = Bill
  context_object_name = "bill"
  payment_form_class = PaymentForm

  def get_success_url(self):
    return reverse('books:bill-detail', args=[self.object.pk])



# Payments

class PaymentUpdateView(generic.UpdateView):
  template_name = "accounting/books/payment_create_or_update.html"
  model = Payment
  form_class = PaymentForm

  def get_success_url(self):
    related_obj = self.object.content_object
    if isinstance(related_obj, Invoice):
      return reverse("books:invoice-detail", args=[related_obj.pk])
    elif isinstance(related_obj, Bill):
      return reverse("books:bill-detail", args=[related_obj.pk])

    logger.warning("Unsupported related object '{}' for "
             "payment '{}'".format(self.object, related_obj))
    return reverse("books:dashboard")


class PaymentDeleteView(generic.DeleteView):
  template_name = "accounting/_forms/delete.html"
  model = Payment
  success_url = reverse_lazy('books:invoice-list')


# ExpenseClaim

class ExpenseClaimListView(
    RestrictToSelectedOrganizationQuerySetMixin,
    SaleListQuerySetMixin,
    generic.ListView):

  template_name = "books/expense_claim/list.html"
  model = ExpenseClaim
  context_object_name = "expense_claims"


class ExpenseClaimCreateView(
    AutoSetSelectedOrganizationMixin,
    SaleLineCreateUpdateMixin,
    generic.CreateView):

  template_name = "books/_sale/create_or_update.html"
  model = ExpenseClaim
  form_class = ExpenseClaimForm
  inlines_formset_pairs = (('line_formset', ExpenseClaimLineFormSet),)
  success_url = reverse_lazy("books:expense_claim-list")

  def get_initial(self):
    initial = super().get_initial()

    orga = organization_manager.get_selected_organization(self.request)
    initial['number'] = ExpenseClaimNumberGenerator().next_number(orga)
    return initial


class ExpenseClaimUpdateView(
    AutoSetSelectedOrganizationMixin,
    SaleLineCreateUpdateMixin,
    generic.UpdateView):

  template_name = "books/_sale/create_or_update.html"
  model = ExpenseClaim
  form_class = ExpenseClaimForm
  inlines_formset_pairs = (('line_formset', ExpenseClaimLineFormSet),)
  success_url = reverse_lazy("books:expense_claim-list")


class ExpenseClaimDeleteView(generic.DeleteView):
  template_name = "accounting/_forms/delete.html"
  model = ExpenseClaim
  success_url = reverse_lazy('books:expense_claim-list')


class ExpenseClaimDetailView(
    PaymentFormMixin,
    AbstractSaleDetailMixin,
    generic.DetailView):

  template_name = "books/_sale/detail.html"
  model = ExpenseClaim
  context_object_name = "expense_claim"
  payment_form_class = PaymentForm

  def get_success_url(self):
    return reverse('books:expense_claim-detail', args=[self.object.pk])
