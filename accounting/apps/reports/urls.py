from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'accounting.apps.reports'

urlpatterns = [

  # Reports
  path('report/',
    views.ReportListView.as_view(),
    name="report-list"),
  path('report/tax/',
    views.TaxReportView.as_view(),
    name="tax-report"),
  path('report/profitloss/',
    views.ProfitAndLossReportView.as_view(),
    name="profit-and-loss-report"),
  path('report/payrun/',
    views.PayRunReportView.as_view(),
    name="pay-run-report"),
  path('report/invoicedetails/',
    views.InvoiceDetailsView.as_view(),
    name="invoice-details-report"),

  # Settings
  path('settings/',
    views.SettingsListView.as_view(),
    name="settings-list"),
  path('settings/business/',
    views.BusinessSettingsUpdateView.as_view(),
    name="settings-business"),
  path('settings/financial/',
    views.FinancialSettingsUpdateView.as_view(),
    name="settings-financial"),
  path('settings/payrun/',
    views.PayRunSettingsUpdateView.as_view(),
    name="settings-payrun"),
]
