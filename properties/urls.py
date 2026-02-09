"""
URL configuration for Properties app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('properties/', views.PropertyListView.as_view(), name='property-list'),
    path('properties/featured/', views.FeaturedPropertiesView.as_view(), name='property-featured'),
    path('properties/<slug:slug>/', views.PropertyDetailView.as_view(), name='property-detail'),
    # Admin
    path('admin/properties/', views.AdminPropertyListCreateView.as_view(), name='admin-property-list-create'),
    path('admin/properties/<int:pk>/', views.AdminPropertyDetailView.as_view(), name='admin-property-detail'),
    path('admin/properties/<int:pk>/images/', views.AdminPropertyImageUploadView.as_view(), name='admin-property-image-upload'),
    path('admin/properties/<int:pk>/images/<int:image_id>/', views.AdminPropertyImageDeleteView.as_view(), name='admin-property-image-delete'),
]
