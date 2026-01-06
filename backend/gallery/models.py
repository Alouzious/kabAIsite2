from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.core.validators import FileExtensionValidator

class GalleryCategory(models.Model):
    """Gallery categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models. BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta: 
        verbose_name = "Gallery Category"
        verbose_name_plural = "Gallery Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    """Gallery images"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Image
    image = ProcessedImageField(
        upload_to='gallery/',
        processors=[ResizeToFit(1200, 900)],
        format='JPEG',
        options={'quality': 90},
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])]
    )
    
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality': 80}
    )
    
    # Metadata
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='images'
    )
    photographer = models.CharField(max_length=100, blank=True)
    event_name = models.CharField(max_length=200, blank=True)
    date_taken = models.DateField(blank=True, null=True)
    
    # Tags
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tags (e.g., workshop, hackathon, team)"
    )
    
    # Display
    order = models.IntegerField(default=0)
    is_active = models. BooleanField(default=True, verbose_name="Show on website")
    is_featured = models.BooleanField(default=False, verbose_name="Featured Image")
    
    # Timestamps
    created_at = models. DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        ordering = ['order', '-date_taken', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        """Return tags as a list"""
        return [tag. strip() for tag in self.tags.split(',')] if self.tags else []