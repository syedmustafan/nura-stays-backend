"""
URL configuration for Accounts (Admin Auth) app.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('login/', views.AdminLoginView.as_view(), name='admin-login'),
    path('logout/', views.AdminLogoutView.as_view(), name='admin-logout'),
    path('verify/', views.AdminVerifyView.as_view(), name='admin-verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('dashboard/stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
]
