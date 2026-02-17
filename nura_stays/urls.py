"""
URL configuration for Nura Stays project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('properties.urls')),
    path('api/', include('reviews.urls')),
    path('api/', include('team.urls')),
    path('api/', include('contact.urls')),
    path('api/admin/', include('accounts.urls')),
]

# Serve media files (uploaded images) in both dev and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
