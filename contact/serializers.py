"""
Serializers for Contact app.
"""
from rest_framework import serializers
from .models import ContactSubmission


class ContactSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for contact form submissions."""

    class Meta:
        model = ContactSubmission
        fields = ['id', 'name', 'email', 'phone', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']
