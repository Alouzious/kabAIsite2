from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit. processors import ResizeToFit
from django.core.validators import FileExtensionValidator

class PartnerCategory(models.Model):
    """Partner categories"""
    CATEGORY_TYPES = [
        ('platinum', 'Platinum Partner'),
        ('gold', 'Gold Partner'),
        ('silver', 'Silver Partner'),
        ('academic', 'Academic Partner'),
        ('technology', 'Technology Partner'),
        ('community', 'Community Partner'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES, default='community')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Partner Category"
        verbose_name_plural = "Partner Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Partner(models.Model):
    """Partners and sponsors"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Logo
    logo = ProcessedImageField(
        upload_to='partners/',
        processors=[ResizeToFit(400, 200)],
        format='PNG',
        options={'quality': 90},
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])],
        help_text="Partner logo (transparent PNG recommended)"
    )
    
    logo_thumbnail = ImageSpecField(
        source='logo',
        processors=[ResizeToFit(200, 100)],
        format='PNG',
        options={'quality': 85}
    )
    
    # Details
    category = models.ForeignKey(
        PartnerCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partners'
    )
    website_url = models.URLField(blank=True, verbose_name="Website URL")
    partnership_level = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g., Gold Sponsor, Strategic Partner"
    )
    partnership_since = models.DateField(blank=True, null=True)
    
    # Display
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    is_active = models.BooleanField(default=True, verbose_name="Show on website")
    is_featured = models.BooleanField(default=False, verbose_name="Featured Partner")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models. DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name