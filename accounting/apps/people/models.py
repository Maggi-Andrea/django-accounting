from decimal import Decimal as D

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Address(models.Model):
 
  # address
  address_line_1 = models.CharField(
    max_length=128,
  )
   
  address_line_2 = models.CharField(
    max_length=128,
    blank=True,
    null=True
  )
   
  city = models.CharField(
    max_length=64
  )
   
  postal_code = models.CharField(
    max_length=7
  )
   
  country = models.CharField(
    max_length=50
  )
   
  def active_address_fields(self):
    """
    Return the non-empty components of the address
    """
    fields = [self.address_line_1, self.address_line_2,
          self.city, self.postal_code, self.country]
    fields = [f.strip() for f in fields if f]
    return fields
 
  def full_address(self, separator="\n"):
    return separator.join(filter(bool, self.active_address_fields()))
    
class FiscalProfile(models.Model):
  
  user = models.OneToOneField(
    to=settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="fiscal_profile",
    primary_key = True,
  )
  
  fiscal_id = models.CharField(
    max_length=20,
  )
  
  address = models.ForeignKey(
    to=Address,
    blank=True,
    null=True,
    on_delete = models.SET_NULL,
  )
  
  def get_absolute_url(self):
    return self.get_detail_url()
  
  def get_detail_url(self):
    return reverse('people:fiscalprofile-detail', args=[self.pk])

  def get_edit_url(self):
    return reverse('people:fiscalprofile-edit', args=[self.pk])
  
class BusinessOrganization(models.Model):
  
  organization = models.ForeignKey(
    to='books.Organization',
    on_delete=models.CASCADE,
    related_name="%(app_label)s_%(class)ss")
  
  class Meta:
    abstract = True
  
class Client(BusinessOrganization):
  
  name = models.CharField(
    max_length=150,
  )
  
  vat_number = models.CharField(
    max_length=30,
    help_text='Fiscal id of the client',
  )
  
  address = models.ForeignKey(
    to=Address,
    blank=True,
    null=True,
    on_delete = models.SET_NULL,
  )

  class Meta:
    unique_together = (
      ('organization', 'vat_number'),
    )
  
  def get_absolute_url(self):
    return self.get_detail_url()
  
  def get_detail_url(self):
    return reverse('people:client-detail', args=[self.pk]) 

  def __str__(self):
    return self.name


class Employee(BusinessOrganization):
  
  first_name = models.CharField(
    max_length=150,
  )
  
  last_name = models.CharField(
    max_length=150,
  )
  
  email = models.EmailField()
  
  address = models.ForeignKey(
    to=Address,
    blank=True,
    null=True,
    on_delete = models.SET_NULL,
  )

  payroll_tax_rate = models.DecimalField(
    max_digits=6,
    decimal_places=5,
    validators=[
      MinValueValidator(D('0')),
      MaxValueValidator(D('1'))
    ]
  )

  salary_follows_profits = models.BooleanField(
    default=False,
  )
  
  shares_percentage = models.DecimalField(
    max_digits=6,
    decimal_places=5,
    validators=[
      MinValueValidator(D('0')),
      MaxValueValidator(D('1'))
    ]
  )

  class Meta:
    pass

  def __str__(self):
    return "{}".format(self.composite_name)

  @property
  def composite_name(self):
    return "{} {}".format(self.first_name, self.last_name)
