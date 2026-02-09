"""
URL configuration for Team app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('team/', views.TeamMemberListView.as_view(), name='team-list'),
    # Admin
    path('admin/team/', views.AdminTeamMemberListCreateView.as_view(), name='admin-team-list-create'),
    path('admin/team/<int:pk>/', views.AdminTeamMemberDetailView.as_view(), name='admin-team-detail'),
]
