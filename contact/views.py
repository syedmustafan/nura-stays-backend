"""
Views for Contact app.
"""
import logging
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer

logger = logging.getLogger(__name__)


class ContactRateThrottle(AnonRateThrottle):
    rate = '5/hour'


class ContactSubmitView(generics.CreateAPIView):
    """Submit a contact form. Saves to DB and sends email to configured address."""
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ContactRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        # Send email (if configured). Save to DB even if email fails.
        to_email = getattr(settings, 'CONTACT_EMAIL_TO', None)
        if to_email:
            try:
                subject = f"Nura Stays Contact: {instance.subject or 'No subject'}"
                body = (
                    f"Name: {instance.name}\n"
                    f"Email: {instance.email}\n"
                    f"Phone: {instance.phone or 'Not provided'}\n"
                    f"Subject: {instance.subject or '—'}\n\n"
                    f"Message:\n{instance.message}"
                )
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[to_email],
                    fail_silently=True,
                )
            except Exception as e:
                logger.exception("Contact form email failed: %s", e)
        return Response(
            {'message': 'Thank you! Your message has been received. We will get back to you soon.'},
            status=status.HTTP_201_CREATED,
        )
