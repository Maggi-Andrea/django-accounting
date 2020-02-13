'''
Created on 12 feb 2020

@author: Andrea
'''
from django.urls import reverse

from dkt.menu import AsideMenu, AsideItem


AsideMenu.add_item(AsideItem(
  "Dashboard",
  reverse('books:dashboard'),
  icon="flaticon2-gear",
))

AsideMenu.add_item(AsideItem(
  "Organizations",
  reverse('books:organization-list'),
  icon="flaticon2-gear",
))

AsideMenu.add_item(AsideItem(
  "Estimates",
  reverse('books:estimate-list'),
  icon="flaticon2-gear",
))

AsideMenu.add_item(AsideItem(
  "Invoices",
  reverse('books:invoice-list'),
  icon="flaticon2-gear",
))

AsideMenu.add_item(AsideItem(
  "Bills",
  reverse('books:bill-list'),
  icon="flaticon2-gear",
))

AsideMenu.add_item(AsideItem(
  "Expense claims",
  reverse('books:expense_claim-list'),
  icon="flaticon2-gear",
))

AsideMenu.add_item(AsideItem(
  "Tax Rates",
  reverse('books:tax_rate-list'),
  icon="flaticon2-gear",
))

AsideMenu.add_item(AsideItem(
  "Contribution Rates",
  reverse('books:contribution_rate-list'),
  icon="flaticon2-gear",
))