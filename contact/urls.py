"""
URL configuration for Contact app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.ContactSubmitView.as_view(), name='contact-submit'),
]
