from django.urls import include
from django.urls import path

urlpatterns = [
#     path('', include('accounting.apps.connect.urls', namespace="connect")),
    path('books/', include('accounting.apps.books.urls', namespace="books")),
    path('people/', include('accounting.apps.people.urls', namespace="people")),
    path('reports/', include('accounting.apps.reports.urls', namespace="reports")),

    # third party
    path('select2/', include('django_select2.urls')),
  ]

