"""
Views for Contact app.
"""
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer


class ContactRateThrottle(AnonRateThrottle):
    rate = '5/hour'


class ContactSubmitView(generics.CreateAPIView):
    """Submit a contact form."""
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ContactRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'message': 'Thank you for your message! We will get back to you soon.'},
            status=status.HTTP_201_CREATED
        )
