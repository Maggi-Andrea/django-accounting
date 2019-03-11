from decimal import Decimal as D

from django.test import TestCase

from . import scenarios

class Alfa_Organization(
    scenarios.Alfa_Invoices_1_2,
    scenarios.Alfa_Organization,
  ):
  pass


class Test_InvoiceQuerySet(Alfa_Organization, TestCase):
  
  def test_turnover(self):
    queryset = self.organization_a.invoices.all()
    self.assertEqual(queryset.turnover_excl_tax(), D('10.00') + D('5.00'))
    self.assertEqual(queryset.turnover_incl_tax(), D('12.00') + D('6.00'))
