"""
Property models for Nura Stays.
"""
from django.db import models
from django.utils.text import slugify
import uuid


class Property(models.Model):
    """Short-term rental property listing."""

    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
        ('villa', 'Villa'),
        ('cottage', 'Cottage'),
        ('penthouse', 'Penthouse'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    location = models.CharField(max_length=255)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    max_guests = models.PositiveIntegerField(default=2)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES, default='apartment')
    amenities = models.JSONField(default=list, blank=True)
    house_rules = models.TextField(blank=True)
    cancellation_policy = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'properties'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img

    def get_average_rating(self):
        from reviews.models import Review
        avg = Review.objects.filter(
            property=self, is_approved=True
        ).aggregate(models.Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else None

    def get_review_count(self):
        from reviews.models import Review
        return Review.objects.filter(property=self, is_approved=True).count()


class PropertyImage(models.Model):
    """Images associated with a property."""

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='properties/')
    is_primary = models.BooleanField(default=False)
    order_index = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order_index', 'created_at']

    def __str__(self):
        return f"Image for {self.property.name} (#{self.order_index})"
