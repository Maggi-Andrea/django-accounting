from django.test import TestCase

from decimal import Decimal as D

from . import scenarios

class Alfa_Organization(
    scenarios.Alfa_Bills_1_2,
    scenarios.Alfa_Organization,
  ):
  pass

class Test_BillLine(Alfa_Organization, TestCase):
  
  def test_prices(self):
    line = self.bill_line_a_1_01
    
    price = line.unit_price
    self.assertEqual('EUR', price.currency)
    self.assertEqual(D('2.0'), price.excl_tax)
    self.assertEqual(D('0.4'), price.tax)
    self.assertEqual(D('2.4'), price.incl_tax)
    
    price = line.line_price
    self.assertEqual('EUR', price.currency)
    self.assertEqual(D('10.0'), price.excl_tax)
    self.assertEqual(D( '2.0'), price.tax)
    self.assertEqual(D('12.0'), price.incl_tax)
    
    self.assertEqual(D('10.0'), line.line_price_excl_tax)
    self.assertEqual(D( '2.0'), line.line_price_tax)
    self.assertEqual(D('12.0'), line.line_price_incl_tax)
    

class Test_Bill(Alfa_Organization, TestCase):
  
  def test_total(self):
    bill = self.bill_a_1
    self.assertEqual(D('10.00'), bill.total_excl_tax)
    self.assertEqual(D( '2.00'), bill.total_tax)
    self.assertEqual(D('12.00'), bill.total_incl_tax)

  def test_get_totals(self):
    bill = self.bill_a_1
    self.assertEqual(D('10.00'), bill.get_total_excl_tax())
    self.assertEqual(D( '2.00'), bill.get_total_tax())
    self.assertEqual(D('12.00'), bill.get_total_incl_tax())
    
  def test_checking(self):
    bill = self.bill_a_1
    
    checks = bill.full_check()
    self.assertEqual(2/3, bill.full_checking_completion())
    self.assertEqual('date_dued: failed.warning - No due date specified', str(checks[2]))
    
    bill.total_excl_tax = D('11.00')
    checks = bill.full_check()
    self.assertEqual(1/3, bill.full_checking_completion())
    self.assertEqual('total_incl_tax: passed', str(checks[0]))
    self.assertEqual("total_excl_tax: failed.error - The computed amount isn't correct, it should be €10.00, please edit and save the bill to fix it.", str(checks[1]))
    self.assertEqual('date_dued: failed.warning - No due date specified', str(checks[2]))
    

class Test_BillQuerySet(Alfa_Organization, TestCase):

  def test_debts_(self):
    queryset = self.organization_a.bills.all()
    self.assertEqual(queryset.debts_excl_tax(), D('10.00') + D('5.00'))
    self.assertEqual(queryset.debts_incl_tax(), D('12.00') + D('6.00'))
