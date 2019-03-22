from django.forms import ModelForm, BaseInlineFormSet
from django.forms.models import inlineformset_factory

from .models import (
  Organization,
  TaxRate,
  ContributionRate,
  Estimate,
  EstimateLine,
  Invoice,
  InvoiceLine,
  InvoiceContribution,
  Bill,
  BillLine,
  ExpenseClaim,
  ExpenseClaimLine,
  Payment)

from accounting.apps.people.forms import AddressFormMixin

from accounting.apps.people.models import Client, Employee
from accounting.apps.people.forms import UserMultipleChoices

from django_select2.forms import ModelSelect2Widget
from tempus_dominus.widgets import DatePicker


class RequiredFirstInlineFormSet(BaseInlineFormSet):
  """
  Used to make empty formset forms required
  See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
#     if len(self.forms) > 0:
#       first_form = self.forms[0]
#       first_form.empty_permitted = False


class SaleLineInlineFormSet(RequiredFirstInlineFormSet):

  def __init__(self, *args, **kwargs):
    orga = kwargs.pop('organization')
    super().__init__(*args, **kwargs)
    for f in self.forms:
      f.restrict_to_organization(orga)


class ClientForOrganizationChoices(ModelSelect2Widget):
  queryset = Client.objects.all()
  search_fields = (
    'name__icontains',
  )

class EmployeeForOrganizationChoices(ModelSelect2Widget):
  queryset = Employee.objects.all()
  search_fields = (
    'name__icontains',
    'last_name__icontains',
    'email__icontains',
  )

class OrganizationForm(AddressFormMixin, ModelForm):

  class Meta:
    model = Organization
    exclude = (
      'owner',
    )
    
    fields = (
      'display_name',
      'legal_name',
      'vat_number',
      'members',
    )
    
    widgets = {
      'members': UserMultipleChoices(),
    }
    


class TaxRateForm(ModelForm):
  class Meta:
    model = TaxRate
    fields = (
      "name",
      "rate",
    )
    
class ContributionRateForm(ModelForm):
  class Meta:
    model = ContributionRate
    fields = (
      "name",
      "rate",
    )


class RestrictLineFormToOrganizationMixin:
  
  restricted_files = None

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
#     instance = kwargs.get('instance', None)
#     if instance:
#       if isinstance(instance, InvoiceLine):
#         organization = instance.invoice.organization
#       elif isinstance(instance, InvoiceContribution):
#         organization = instance.invoice.organization
#       elif isinstance(instance, BillLine):
#         organization = instance.bill.organization
#       elif isinstance(instance, ExpenseClaimLine):
#         organization = instance.expense_claim.organization
#       elif isinstance(instance, EstimateLine):
#         organization = instance.invoice.organization
#       else:
#         raise NotImplementedError("The mixin has been applied to a "
#                       "form model that is not supported")
#       self.restrict_to_organization(organization)
#     else:
#       pass

  def restrict_to_organization(self, organization):
    if self.restricted_files:
      for filed in self.restricted_files:
        new_queryset = self.fields[filed].queryset.filter(organization=organization)
        print(filed, self.fields[filed].queryset, new_queryset)
        self.fields[filed].queryset = new_queryset


class EstimateForm(ModelForm):

  class Meta:
    model = Estimate
    fields = (
      "number",
      "client",
      "date_issued",
      "date_dued",
    )
    widgets = {
      'client' : ClientForOrganizationChoices(),
      'date_issued': DatePicker(
        attrs={
          'append': 'fa fa-calendar',
          'input_toggle': True,
          'icon_toggle': True,
        }
      ),
      'date_dued': DatePicker(
        attrs={
          'append': 'fa fa-calendar',
          'input_toggle': True,
          'icon_toggle': True,
        }
      ),
    }


class EstimateLineForm(RestrictLineFormToOrganizationMixin, ModelForm):
  
  restricted_files = ('tax_rate', )
  
  class Meta:
    model = EstimateLine
    fields = (
      "label",
      "description",
      "unit_price_excl_tax",
      "quantity",
      "tax_rate",
    )


EstimateLineFormSet = inlineformset_factory(Estimate,
                      EstimateLine,
                      form=EstimateLineForm,
                      formset=SaleLineInlineFormSet,
                      min_num=1,
                      extra=0)


class InvoiceForm(ModelForm):

  class Meta:
    model = Invoice
    fields = (
      "number",
      "client",
      "date_issued",
      "date_dued",
    )
    widgets = {
      'client' : ClientForOrganizationChoices(),
      'date_issued': DatePicker(
        attrs={
          'append': 'fa fa-calendar',
          'input_toggle': True,
          'icon_toggle': True,
        }
      ),
      'date_dued': DatePicker(
        attrs={
          'append': 'fa fa-calendar',
          'input_toggle': True,
          'icon_toggle': True,
        }
      ),
    }


class InvoiceLineForm(RestrictLineFormToOrganizationMixin, ModelForm):
  
  restricted_files = ('tax_rate', )
  
  class Meta:
    model = InvoiceLine
    fields = (
      "label",
      "description",
      "unit_price_excl_tax",
      "quantity",
      "tax_rate",
    )


InvoiceLineFormSet = inlineformset_factory(
  parent_model = Invoice,
  model = InvoiceLine,
  form=InvoiceLineForm,
  formset=SaleLineInlineFormSet,
  min_num=1,
  extra=0,
)

class InvoiceContributionForm(RestrictLineFormToOrganizationMixin, ModelForm):
  
  restricted_files = ('contribution_rate', 'tax_rate', )
  
  class Meta:
    model = InvoiceContribution
    fields = (
      "contribution_rate",
      "tax_rate",
    )

InvoiceContributionFormSet = inlineformset_factory(
  parent_model = Invoice,
  model = InvoiceContribution,
  form = InvoiceContributionForm,
  formset = SaleLineInlineFormSet,
#   fk_name = '?',
  extra = 1,
  min_num = 0,
)


class BillForm(ModelForm):

  class Meta:
    model = Bill
    fields = (
      "number",
      "client",
      "date_issued",
      "date_dued",
    )
    widgets = {
      'client' : ClientForOrganizationChoices(),
      'date_issued': DatePicker(
        attrs={
          'append': 'fa fa-calendar',
          'input_toggle': True,
          'icon_toggle': True,
        }
      ),
      'date_dued': DatePicker(
        attrs={
          'append': 'fa fa-calendar',
          'input_toggle': True,
          'icon_toggle': True,
        }
      ),
    }


class BillLineForm(RestrictLineFormToOrganizationMixin, ModelForm):
  
  restricted_files = ('tax_rate', )
  
  class Meta:
    model = BillLine
    fields = (
      "label",
      "description",
      "unit_price_excl_tax",
      "quantity",
      "tax_rate",
    )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


BillLineFormSet = inlineformset_factory(Bill,
                    BillLine,
                    form=BillLineForm,
                    formset=SaleLineInlineFormSet,
                    min_num=1,
                    extra=0)


class ExpenseClaimForm(ModelForm):
  class Meta:
    model = ExpenseClaim
    fields = (
      "number",
      "employee",
      "date_issued",
      "date_dued",
    )
    widgets = {
      'employee': EmployeeForOrganizationChoices(),
      'date_issued': DatePicker(
        attrs={
          'append': 'fa fa-calendar',
          'input_toggle': True,
          'icon_toggle': True,
        }
      ),
      'date_dued': DatePicker(
        attrs={
          'append': 'fa fa-calendar',
          'input_toggle': True,
          'icon_toggle': True,
        }
      ),
    }


class ExpenseClaimLineForm(RestrictLineFormToOrganizationMixin, ModelForm):
  
  restricted_files = ('tax_rate', )
  
  class Meta:
    model = ExpenseClaimLine
    fields = (
      "label",
      "description",
      "unit_price_excl_tax",
      "quantity",
      "tax_rate",
    )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


ExpenseClaimLineFormSet = inlineformset_factory(ExpenseClaim,
                        ExpenseClaimLine,
                        form=ExpenseClaimLineForm,
                        formset=SaleLineInlineFormSet,
                        min_num=1,
                        extra=0)


class PaymentForm(ModelForm):
  class Meta:
    model = Payment
    fields = (
      "amount",
      "reference",
      "detail",
      "date_paid",
    )
    widgets = {
      'date_paid': DatePicker(
        attrs={
          'append': 'fa fa-calendar',
          'input_toggle': True,
          'icon_toggle': True,
        }
      ),
    }
