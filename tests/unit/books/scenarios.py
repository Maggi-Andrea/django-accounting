'''
Created on 09 mar 2019

@author: Andrea
'''
from django_dynamic_fixture import G

from decimal import Decimal as D

from accounting.apps.books.models import Organization
from accounting.apps.books.models import TaxRate
from accounting.apps.books.models import ContributionRate


from accounting.apps.books.models import Bill
from accounting.apps.books.models import BillLine

from accounting.apps.books.models import Invoice
from accounting.apps.books.models import InvoiceLine, InvoiceContribution

class Alfa_Organization:
  
  def setUp(self):
    super().setUp()
    self.organization_a = G(Organization, display_name='Organization Alfa')
    self.esente_a = G(TaxRate, organization=self.organization_a, name="Esente", rate=D('0.0'))
    self.iva20_a = G(TaxRate, organization=self.organization_a, name="Iva 20", rate=D('0.20'))
    
    self.ritenura4_a = G(ContributionRate, organization=self.organization_a, name="Contributo 4%", rate=D('0.04'))

class Alfa_Bill_1:
  
  def setUp(self):
    super().setUp()
    self.bill_a_1 = G(
      Bill,
      organization=self.organization_a,
      number=1,
    )
    
    self.bill_line_a_1_01 = G(
      BillLine,
      bill=self.bill_a_1,
      unit_price_excl_tax=D('2.0'),
      quantity=D('5'),
      tax_rate=self.iva20_a,
    )
    
    self.bill_a_1.compute_totals().save()
    
  
class Alfa_Bills_1_2(Alfa_Bill_1):
  
  def setUp(self):
    super().setUp()
    
    
    self.bill_a_2 = G(
      Bill,
      organization=self.organization_a,
      number=2,
      total_excl_tax=D('5.00'),
      total_incl_tax=D('6.00'),
    )
    
class Alfa_Invoice_1:
  
  def setUp(self):
    super().setUp()
    
    self.invoice_a_1 = G(
      Invoice,
      organization = self.organization_a,
      number = 1,
    )
    
    self.invoice_line_a_1_01 = G(
      InvoiceLine,
      invoice= self.invoice_a_1,
      label = 'Consulenza',
      unit_price_excl_tax = D('2000'),
      tax_rate = self.esente_a,
      quantity = 1,
    )
    
    self.invoice_contribution_a_1_01 = G(
      InvoiceContribution,
      invoice = self.invoice_a_1,
      contribution_rate = self.ritenura4_a,
      tax_rate = self.esente_a,
    )
    
    self.invoice_a_1.compute_totals().save()

    

class Alfa_Invoices_1_2(Alfa_Invoice_1):
  
  def setUp(self):
    super().setUp()
    
    self.invoice_a_2 = G(
      Invoice,
      organization=self.organization_a,
      number=2,
      total_excl_tax=D('5.00'),
      total_incl_tax=D('6.00'),
    )
