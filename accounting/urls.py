from django.urls import include
from django.urls import path

urlpatterns = [
    path('', include('accounting.apps.connect.urls')),
    path('books/', include('accounting.apps.books.urls')),
    path('people/', include('accounting.apps.people.urls')),
    path('reports/', include('accounting.apps.reports.urls')),

    # third party
    path('select2/', include('django_select2.urls')),
  ]

