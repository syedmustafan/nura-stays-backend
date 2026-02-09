"""
URL configuration for Reviews app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('reviews/stats/', views.ReviewStatsView.as_view(), name='review-stats'),
    path('reviews/property/<int:property_id>/', views.PropertyReviewsView.as_view(), name='property-reviews'),
    # Admin
    path('admin/reviews/', views.AdminReviewListCreateView.as_view(), name='admin-review-list-create'),
    path('admin/reviews/<int:pk>/', views.AdminReviewDetailView.as_view(), name='admin-review-detail'),
]
