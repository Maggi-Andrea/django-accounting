from django.urls import path

from . import views

app_name = 'connect'

urlpatterns = [

  path('',
       views.RootRedirectionView.as_view(),
       name="root"),

    # Step by step
  path('getting-started/',
       views.GettingStartedView.as_view(),
       name="getting_started")
]
