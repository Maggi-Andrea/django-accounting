from decimal import Decimal as D

from django.test import TestCase

from . import scenarios

class Alfa_Organization(
    scenarios.Alfa_Invoice_1,
    scenarios.Alfa_Organization,
  ):
  pass


class Test_InvoiceLine(Alfa_Organization, TestCase):
  
  def unit_price(self):
    line = self.invoice_line_a_1_01
    
    price = line.unit_price
    self.assertEqual('EUR', price.currency)
    self.assertEqual(D('2000.0'), price.excl_tax)
    self.assertEqual(D(   '0.0'), price.tax)
    self.assertEqual(D('2000.0'), price.incl_tax)
    
  def line_price(self):
    line = self.invoice_line_a_1_01
    price = line.line_price
    self.assertEqual('EUR', price.currency)
    self.assertEqual(D('2000.0'), price.excl_tax)
    self.assertEqual(D(   '0.0'), price.tax)
    self.assertEqual(D('2000.0'), price.incl_tax)
    
    self.assertEqual(D('2000.0'), line.line_price_excl_tax)
    self.assertEqual(D(   '0.0'), line.line_price_tax)
    self.assertEqual(D('2000.0'), line.line_price_incl_tax)
    
class Test_InvoiceWithholding(Alfa_Organization, TestCase):
  
  def test_amount(self):
    contribution = self.invoice_contribution_a_1_01
    
    price = contribution.amount
    self.assertEqual('EUR', price.currency)
    self.assertEqual(D('80.00'), price.excl_tax)
    self.assertEqual(D(' 0.00'), price.tax)
    self.assertEqual(D('80.00'), price.incl_tax)
    
  def test_contribution(self):
    contribution = self.invoice_contribution_a_1_01
    
    self.assertEqual(D('80.0'), contribution.contribution_excl_tax)
    self.assertEqual(D(' 0.0'), contribution.contribution_tax)
    self.assertEqual(D('80.0'), contribution.contribution_incl_tax)
    
class Test_Invoice(Alfa_Organization, TestCase):
  
  def test_total(self):
    invoice = self.invoice_a_1
    self.assertEqual(D('2080.00'), invoice.total_excl_tax)
    self.assertEqual(D(   '0.00'), invoice.total_tax)
    self.assertEqual(D('2080.00'), invoice.total_incl_tax)

  def test_get_totals(self):
    invoice = self.invoice_a_1
    self.assertEqual(D('2080.00'), invoice.get_total_excl_tax())
    self.assertEqual(D(   '0.00'), invoice.get_total_tax())
    self.assertEqual(D('2080.00'), invoice.get_total_incl_tax())
    
  def test_checking(self):
    invoice = self.invoice_a_1
    
    checks = invoice.full_check()
    self.assertEqual(2/3, invoice.full_checking_completion())
    self.assertEqual('date_dued: failed.warning - No due date specified', str(checks[2]))
    
    invoice.total_excl_tax = D('11.00')
    checks = invoice.full_check()
    self.assertEqual(1/3, invoice.full_checking_completion())
    self.assertEqual('total_incl_tax: passed', str(checks[0]))
    self.assertEqual("total_excl_tax: failed.error - The computed amount isn't correct, it should be €2,080.00, please edit and save the invoice to fix it.", str(checks[1]))
    self.assertEqual('date_dued: failed.warning - No due date specified', str(checks[2]))


class Test_InvoiceQuerySet(Alfa_Organization, TestCase):

  def test_turnover(self):
    queryset = self.organization_a.invoices.all()
    self.assertEqual(queryset.turnover_excl_tax(), D('2080.00'))
    self.assertEqual(queryset.turnover_incl_tax(), D('2080.00'))
