from django.forms import ModelForm, BaseInlineFormSet
from django.forms.models import inlineformset_factory

from .models import (
  Organization,
  TaxRate,
  Estimate,
  EstimateLine,
  Invoice,
  InvoiceLine,
  Bill,
  BillLine,
  ExpenseClaim,
  ExpenseClaimLine,
  Payment)
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
    if len(self.forms) > 0:
      first_form = self.forms[0]
      first_form.empty_permitted = False


class SaleInlineLineFormSet(RequiredFirstInlineFormSet):

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
    'first_name__icontains',
    'last_name__icontains',
    'email__icontains',
  )

class OrganizationForm(ModelForm):

  class Meta:
    model = Organization
    fields = (
      "display_name",
      "legal_name",
      "members",
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


class RestrictLineFormToOrganizationMixin(object):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    instance = kwargs.get('instance', None)
    if instance:
      if isinstance(instance, InvoiceLine):
        organization = instance.invoice.organization
      elif isinstance(instance, BillLine):
        organization = instance.bill.organization
      elif isinstance(instance, ExpenseClaimLine):
        organization = instance.expense_claim.organization
      elif isinstance(instance, EstimateLine):
        organization = instance.invoice.organization
      else:
        raise NotImplementedError("The mixin has been applied to a "
                      "form model that is not supported")
      self.restrict_to_organization(organization)

  def restrict_to_organization(self, organization):
    self.fields['tax_rate'].queryset = organization.tax_rates.all()


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
                      formset=SaleInlineLineFormSet,
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


class InvoiceLineForm(RestrictLineFormToOrganizationMixin,
            ModelForm):
  class Meta:
    model = InvoiceLine
    fields = (
      "label",
      "description",
      "unit_price_excl_tax",
      "quantity",
      "tax_rate",
    )


InvoiceLineFormSet = inlineformset_factory(Invoice,
                       InvoiceLine,
                       form=InvoiceLineForm,
                       formset=SaleInlineLineFormSet,
                       min_num=1,
                       extra=0)


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


class BillLineForm(RestrictLineFormToOrganizationMixin,
           ModelForm):
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
                    formset=SaleInlineLineFormSet,
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


class ExpenseClaimLineForm(RestrictLineFormToOrganizationMixin,
               ModelForm):
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
                        formset=SaleInlineLineFormSet,
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
