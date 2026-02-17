"""
Views for Accounts (Admin Auth) app.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenRefreshView
from django.db.models import Avg, Count
from properties.models import Property
from reviews.models import Review
from team.models import TeamMember


class AdminLoginView(APIView):
    """Admin login endpoint."""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Authenticate
        user = authenticate(username=user.username, password=password)
        if user is None or not user.is_staff:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.get_full_name() or user.username,
            }
        })


class AdminLogoutView(APIView):
    """Admin logout endpoint - blacklist refresh token."""
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class AdminVerifyView(APIView):
    """Verify current token and return user info."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.get_full_name() or user.username,
            }
        })


class DashboardStatsView(APIView):
    """Get dashboard overview statistics."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_properties = Property.objects.count()
        active_properties = Property.objects.filter(is_active=True).count()
        total_reviews = Review.objects.count()
        approved_reviews = Review.objects.filter(is_approved=True).count()
        avg_rating = Review.objects.filter(is_approved=True).aggregate(
            avg=Avg('rating')
        )['avg']
        total_team = TeamMember.objects.count()

        return Response({
            'total_properties': total_properties,
            'active_properties': active_properties,
            'total_reviews': total_reviews,
            'approved_reviews': approved_reviews,
            'average_rating': round(avg_rating, 1) if avg_rating else 0,
            'total_team_members': total_team,
        })
