"""
Review models for Nura Stays.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """Guest review for a property or general review."""

    property = models.ForeignKey(
        'properties.Property',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews'
    )
    guest_name = models.CharField(max_length=255)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.guest_name} - {self.rating}★"
