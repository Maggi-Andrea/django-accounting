'''
Created on 09 mar 2019

@author: Andrea
'''
from django.test import TestCase

from decimal import Decimal as D

from . import scenarios

class Test_NewOrganization(scenarios.Alfa_Organization, TestCase):
  
  def test_organization_alfa(self):
    organization = self.organization_a
    self.assertEqual('Organization Alfa', organization.name)
    
    self.assertEqual(D('0'), organization.turnover_excl_tax)
    self.assertEqual(D('0'), organization.turnover_incl_tax)
    
    self.assertEqual(D('0'), organization.debts_excl_tax)
    self.assertEqual(D('0'), organization.debts_incl_tax)
    
    self.assertEqual(D('0'), organization.profits)
    self.assertEqual(D('0'), organization.collected_tax)
    self.assertEqual(D('0'), organization.deductible_tax)
    self.assertEqual(D('0'), organization.tax_provisionning)
    self.assertEqual(D('0'), organization.overdue_total)
  

class Test_DebtsOrganization(scenarios.Alfa_Bills_1_2, scenarios.Alfa_Organization, TestCase):
  
  def test_display_name(self):
    organization = self.organization_a
    self.assertEqual('Organization Alfa', organization.name)
    
  def test_(self):
    organization = self.organization_a
    self.assertEqual(D(  '0'), organization.turnover_excl_tax)
    self.assertEqual(D(  '0'), organization.turnover_incl_tax)
    
    self.assertEqual(D( '15'), organization.debts_excl_tax)
    self.assertEqual(D( '18'), organization.debts_incl_tax)
    
    self.assertEqual(D('-15'), organization.profits)
    self.assertEqual(D(  '0'), organization.collected_tax)
    self.assertEqual(D(  '3'), organization.deductible_tax)
    self.assertEqual(D( '-3'), organization.tax_provisionning)
    self.assertEqual(D(  '0'), organization.overdue_total)
    
    