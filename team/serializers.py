"""
Serializers for Team app.
"""
from rest_framework import serializers
from .models import TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for team member display."""
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = [
            'id', 'name', 'role', 'bio', 'photo', 'photo_url',
            'social_links', 'order_index', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        elif obj.photo:
            return obj.photo.url
        return None
