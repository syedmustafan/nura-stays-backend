"""
Serializers for Contact app.
"""
from rest_framework import serializers
from .models import ContactSubmission


class ContactSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for contact form submissions. Validates name, email, message as required."""

    class Meta:
        model = ContactSubmission
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        if not (data.get('name') or '').strip():
            raise serializers.ValidationError({'name': 'Name is required.'})
        if not (data.get('email') or '').strip():
            raise serializers.ValidationError({'email': 'Email is required.'})
        if not (data.get('message') or '').strip():
            raise serializers.ValidationError({'message': 'Message is required.'})
        return data
