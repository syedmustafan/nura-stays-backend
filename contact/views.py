"""
Views for Contact app.
"""
import logging
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer

logger = logging.getLogger(__name__)


# ─── Admin Leads API (for Admin Dashboard frontend) ─────────────────────────────

class AdminLeadListView(generics.ListAPIView):
    """Admin: list all contact submissions (leads) with optional search and filter."""
    queryset = ContactSubmission.objects.all().order_by('-created_at')
    serializer_class = ContactSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from django.db.models import Q
        qs = super().get_queryset()
        search = self.request.query_params.get('search', '').strip()
        is_read = self.request.query_params.get('is_read')
        if search:
            qs = qs.filter(
                Q(name__icontains=search) | Q(email__icontains=search)
                | Q(message__icontains=search) | Q(subject__icontains=search)
            )
        if is_read is not None and is_read != '':
            qs = qs.filter(is_read=is_read.lower() == 'true')
        return qs


class AdminLeadDetailView(generics.RetrieveUpdateAPIView):
    """Admin: retrieve or partial update a single lead (e.g. mark as read/unread)."""
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch']


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
