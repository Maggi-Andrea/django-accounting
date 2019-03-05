from django.urls import path

from . import views

app_name = 'accounting.apps.connect'

urlpatterns = [

  path('',
       views.RootRedirectionView.as_view(),
       name="root"),

    # Step by step
  path('getting-started/',
       views.GettingStartedView.as_view(),
       name="getting-started")
]
