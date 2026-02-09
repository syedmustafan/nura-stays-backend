"""
Serializers for Reviews app.
"""
from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for public review display."""
    property_name = serializers.CharField(source='property.name', read_only=True, default=None)

    class Meta:
        model = Review
        fields = [
            'id', 'property', 'property_name', 'guest_name',
            'rating', 'review_text', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ReviewAdminSerializer(serializers.ModelSerializer):
    """Serializer for admin CRUD operations on reviews."""
    property_name = serializers.CharField(source='property.name', read_only=True, default=None)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
