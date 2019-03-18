from django.forms import ModelForm
from django.contrib.auth import get_user_model

from .models import Client, Employee, FiscalProfile, Address

from django_select2.forms import ModelSelect2Mixin
from django_select2.forms import ModelSelect2MultipleWidget

# from django_select2.fields import (
#   AutoModelSelect2Field,
#   AutoModelSelect2MultipleField)


class AddressForm(ModelForm):
  
  class Meta:
    model = Address
    
    fields = (
      "address_line_1",
      "address_line_2",
      "city",
      "postal_code",
      "country",
    )
    
class AddressFormMixin:
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    post_data = kwargs.get('data', None)

    if post_data:
      # We received POST data, fill the forms in with the address data returned.
      self.address_data = {
        key: post_data[key]
        for key in post_data
          if key.startswith('address-')
        }
        
      self.address_form = AddressForm(
        instance=self.instance.address,
        prefix='address',
        data=self.address_data
      )
    
    else:
      # We didn't get any POST data
      # Fill the forms in with the address data from the linked address, or create a blank form if none exists.
      if self.instance.address:
        # Get the delivery address form
        self.address_form = AddressForm(
          instance=self.instance.address,
          prefix='address'
        )
      else:
        # There is no linked delivery address. Create a blank form.
        self.address_form = AddressForm(
          prefix='address',
        )
        
  def is_valid(self):
    if not self.address_form.is_valid():
      return False
    return super().is_valid()
  
  def save(self, *args, **kwargs):
    address = self.address_form.save()
    objects_ = super().save(commit=False)
    objects_.address = address
    return super().save(*args, **kwargs)

class FiscalProfileForm(AddressFormMixin, ModelForm):
  class Meta:
    model = FiscalProfile
    fields = (
      'fiscal_id',
    )
  

class ClientForm(AddressFormMixin, ModelForm):
  class Meta:
    model = Client
    fields = (
      "name",
    )


class EmployeeForm(AddressFormMixin, ModelForm):
  class Meta:
    model = Employee
    fields = (
      "first_name",
      "last_name",
      "email",

      "payroll_tax_rate",

      "salary_follows_profits",
      "shares_percentage",

    )


# TODO: avoid calling this in the global scope, can lead to circular imports
User = get_user_model()


class UserChoices(ModelSelect2Mixin):
  queryset = User.objects.all()
  search_fields = (
    'first_name__icontains',
    'last_name__icontains',
    'username__icontains',
    'email__icontains',
  )


class UserMultipleChoices(ModelSelect2MultipleWidget):
  queryset = User.objects.all()
  search_fields = (
    'first_name__icontains',
    'last_name__icontains',
    'username__icontains',
    'email__icontains',
  )
