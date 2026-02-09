"""
Views for Properties app.
"""
from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from .models import Property, PropertyImage
from .serializers import (
    PropertyListSerializer,
    PropertyDetailSerializer,
    PropertyAdminSerializer,
    PropertyImageSerializer,
)
from .filters import PropertyFilter


# ─── Public Views ────────────────────────────────────────────────────────────

class PropertyListView(generics.ListAPIView):
    """List all active properties with filters, search, and pagination."""
    serializer_class = PropertyListSerializer
    permission_classes = [AllowAny]
    filterset_class = PropertyFilter
    search_fields = ['name', 'location', 'description']
    ordering_fields = ['price_per_night', 'created_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        from django.db.models import Q
        return Property.objects.filter(is_active=True).annotate(
            average_rating=Avg('reviews__rating', filter=Q(reviews__is_approved=True)),
            review_count=Count('reviews', filter=Q(reviews__is_approved=True)),
        )


class PropertyDetailView(generics.RetrieveAPIView):
    """Get a single property by slug."""
    serializer_class = PropertyDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        from django.db.models import Q
        return Property.objects.filter(is_active=True).annotate(
            average_rating=Avg('reviews__rating', filter=Q(reviews__is_approved=True)),
            review_count=Count('reviews', filter=Q(reviews__is_approved=True)),
        )


class FeaturedPropertiesView(generics.ListAPIView):
    """Get featured properties."""
    serializer_class = PropertyListSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        from django.db.models import Q
        return Property.objects.filter(
            is_active=True, is_featured=True
        ).annotate(
            average_rating=Avg('reviews__rating', filter=Q(reviews__is_approved=True)),
            review_count=Count('reviews', filter=Q(reviews__is_approved=True)),
        )[:6]


# ─── Admin Views ─────────────────────────────────────────────────────────────

class AdminPropertyListCreateView(generics.ListCreateAPIView):
    """Admin: list all properties or create a new one."""
    queryset = Property.objects.all()
    serializer_class = PropertyAdminSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'location']
    ordering_fields = ['price_per_night', 'created_at', 'name']


class AdminPropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: retrieve, update, or delete a property."""
    queryset = Property.objects.all()
    serializer_class = PropertyAdminSerializer
    permission_classes = [IsAuthenticated]


class AdminPropertyImageUploadView(APIView):
    """Admin: upload images for a property."""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            prop = Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response(
                {'error': 'Property not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        images = request.FILES.getlist('images')
        if not images:
            images = request.FILES.getlist('image')

        if not images:
            return Response(
                {'error': 'No images provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_images = []
        is_primary = request.data.get('is_primary', 'false').lower() == 'true'
        current_count = prop.images.count()

        for i, img_file in enumerate(images):
            img = PropertyImage.objects.create(
                property=prop,
                image=img_file,
                is_primary=is_primary and i == 0,
                order_index=current_count + i,
            )
            created_images.append(img)

        serializer = PropertyImageSerializer(
            created_images, many=True, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminPropertyImageDeleteView(APIView):
    """Admin: delete a property image."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, image_id):
        try:
            image = PropertyImage.objects.get(pk=image_id, property_id=pk)
        except PropertyImage.DoesNotExist:
            return Response(
                {'error': 'Image not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        image.image.delete(save=False)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
