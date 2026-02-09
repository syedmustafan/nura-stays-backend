"""
Team member models for Nura Stays.
"""
from django.db import models


class TeamMember(models.Model):
    """Team member profile."""

    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    social_links = models.JSONField(default=dict, blank=True)
    order_index = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order_index', 'name']

    def __str__(self):
        return f"{self.name} - {self.role}"
