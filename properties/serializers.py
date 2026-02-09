"""
Serializers for Properties app.
"""
from rest_framework import serializers
from .models import Property, PropertyImage


class PropertyImageSerializer(serializers.ModelSerializer):
    """Serializer for property images."""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'image_url', 'is_primary', 'order_index', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return None


class PropertyListSerializer(serializers.ModelSerializer):
    """Serializer for property list view (lightweight)."""
    primary_image = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'name', 'slug', 'location', 'short_description',
            'price_per_night', 'bedrooms', 'bathrooms', 'max_guests',
            'property_type', 'amenities', 'is_featured', 'primary_image',
            'average_rating', 'review_count', 'created_at',
        ]

    def get_primary_image(self, obj):
        img = obj.images.filter(is_primary=True).first()
        if not img:
            img = obj.images.first()
        if img:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(img.image.url)
            return img.image.url
        return None


class PropertyDetailSerializer(serializers.ModelSerializer):
    """Serializer for property detail view (full)."""
    images = PropertyImageSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'name', 'slug', 'location', 'description', 'short_description',
            'price_per_night', 'bedrooms', 'bathrooms', 'max_guests',
            'property_type', 'amenities', 'house_rules', 'cancellation_policy',
            'is_active', 'is_featured', 'images', 'average_rating',
            'review_count', 'created_at', 'updated_at',
        ]


class PropertyAdminSerializer(serializers.ModelSerializer):
    """Serializer for admin CRUD operations on properties."""
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
