"""
Admin-only URL configuration for Contact app (Leads).
Mounted at api/admin/leads/
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdminLeadListView.as_view(), name='admin-lead-list'),
    path('<int:pk>/', views.AdminLeadDetailView.as_view(), name='admin-lead-detail'),
]
