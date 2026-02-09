"""
Views for Reviews app.
"""
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Count
from .models import Review
from .serializers import ReviewSerializer, ReviewAdminSerializer


# ─── Public Views ────────────────────────────────────────────────────────────

class ReviewListView(generics.ListAPIView):
    """List all approved reviews with optional filters."""
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['rating', 'property']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        return Review.objects.filter(is_approved=True).select_related('property')


class PropertyReviewsView(generics.ListAPIView):
    """Get reviews for a specific property."""
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        property_id = self.kwargs['property_id']
        return Review.objects.filter(
            property_id=property_id, is_approved=True
        ).select_related('property')


class ReviewStatsView(APIView):
    """Get overall review statistics."""
    permission_classes = [AllowAny]

    def get(self, request):
        stats = Review.objects.filter(is_approved=True).aggregate(
            average_rating=Avg('rating'),
            total_reviews=Count('id'),
        )
        # Rating distribution
        distribution = {}
        for i in range(1, 6):
            distribution[str(i)] = Review.objects.filter(
                is_approved=True, rating=i
            ).count()

        return Response({
            'average_rating': round(stats['average_rating'], 1) if stats['average_rating'] else 0,
            'total_reviews': stats['total_reviews'],
            'distribution': distribution,
        })


# ─── Admin Views ─────────────────────────────────────────────────────────────

class AdminReviewListCreateView(generics.ListCreateAPIView):
    """Admin: list all reviews or create a new one."""
    queryset = Review.objects.all().select_related('property')
    serializer_class = ReviewAdminSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['rating', 'is_approved', 'property']
    ordering_fields = ['created_at', 'rating']


class AdminReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: retrieve, update, or delete a review."""
    queryset = Review.objects.all()
    serializer_class = ReviewAdminSerializer
    permission_classes = [IsAuthenticated]
