'''
Created on 12 feb 2020

@author: Andrea
'''
from django.urls import reverse

from dkt.menu import AsideMenu, AsideItem, TopbarUser

_organizations = [
  AsideItem(
    "List",
    reverse('books:organization-list'),
    icon="flaticon2-gear",
  ),
  AsideItem(
    "Selector",
    reverse('books:organization-selector'),
    icon="flaticon2-gear",
  ),
]

AsideMenu.add_item(AsideItem(
  "Organizations",
  reverse('books:organization-list'),
  children = _organizations,
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

_people = [
  AsideItem(
    "Clients",
    reverse('people:client-list'),
  ),
  AsideItem(
    "Employees",
    reverse('people:employee-list'),
  ),
]

AsideMenu.add_item(AsideItem(
  "People",
  reverse('people:client-list'),
  children = _people,
  icon="flaticon-customer",
))

_reports = [
  AsideItem(
    "Reports",
    reverse('reports:report-list'),
    children=[
      AsideItem(
        "Tax",
        reverse('reports:report-tax'),
      ),
      AsideItem(
        "Profit and Loss",
        reverse('reports:report-profit_and_loss'),
      ),
      AsideItem(
        "Payrun",
        reverse('reports:report-payrun'),
      ),
      AsideItem(
        "Invoice Details",
        reverse('reports:report-invoice_details'),
      ),
    ]
  ),
  AsideItem(
    "Settings",
    reverse('reports:settings-list'),
    children=[
      AsideItem(
        "Business",
        reverse('reports:settings-business'),
      ),
      AsideItem(
        "Financial",
        reverse('reports:settings-financial'),
      ),
      AsideItem(
        "Pay Run",
        reverse('reports:settings-payrun'),
      ),
    ]
  ),
]

AsideMenu.add_item(AsideItem(
  "Reports",
  "/reports",
  children = _reports,
  icon="flaticon-customer",
))

def _fiscalprofile_url(request):
  user = getattr(request, 'user', None)
  if user and user.is_authenticated:
    return reverse('people:fiscalprofile-detail', kwargs = dict(pk=user.pk))
  return ''

TopbarUser.add_item(
  AsideItem(
    title="Fiscal Profile",
    url = _fiscalprofile_url,
    check=lambda request: request.user.is_authenticated,
  )
)

TopbarUser.add_item(
  AsideItem(
    title = "Sign Out",
    url = reverse('people:logout'),
    weight=10,
    icon="flaticon2-calendar-3",
    check=lambda request: request.user.is_authenticated,
    widget = 'btn'
  ),
)

TopbarUser.add_item(
  AsideItem(
    title = "Log In",
    url = reverse('people:login'),
    weight=10,
    icon="flaticon2-calendar-3",
    check=lambda request: not request.user.is_authenticated,
    widget = 'btn'
  ),
)


