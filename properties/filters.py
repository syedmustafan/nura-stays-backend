"""
Filters for Properties app.
"""
import django_filters
from .models import Property


class PropertyFilter(django_filters.FilterSet):
    """Filter set for properties."""
    min_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='lte')
    min_bedrooms = django_filters.NumberFilter(field_name='bedrooms', lookup_expr='gte')
    max_bedrooms = django_filters.NumberFilter(field_name='bedrooms', lookup_expr='lte')
    property_type = django_filters.CharFilter(field_name='property_type', lookup_expr='exact')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = Property
        fields = ['property_type', 'bedrooms', 'bathrooms', 'is_featured']
