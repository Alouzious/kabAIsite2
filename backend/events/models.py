from django.db import models
from imagekit. models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django. core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.utils import timezone

class EventCategory(models.Model):
    """Event categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class (e.g., fa-calendar)")
    color = models.CharField(max_length=7, default="#007bff", help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    
    created_at = models. DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Event(models.Model):
    """Events (past and upcoming)"""
    EVENT_STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    
    # Image
    image = ProcessedImageField(
        upload_to='events/',
        processors=[ResizeToFill(800, 600)],
        format='JPEG',
        options={'quality': 85},
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])]
    )
    
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality':  80}
    )
    
    # Event Details
    category = models.ForeignKey(
        EventCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True, help_text="For multi-day events")
    location = models.CharField(max_length=200)
    venue_details = models.TextField(blank=True, help_text="Additional venue information")
    
    # Registration
    registration_link = models.URLField(blank=True, help_text="External registration link")
    registration_deadline = models.DateField(blank=True, null=True)
    max_participants = models.IntegerField(blank=True, null=True, help_text="Maximum number of participants")
    
    # Status
    status = models.CharField(max_length=20, choices=EVENT_STATUS_CHOICES, default='upcoming')
    is_published = models.BooleanField(default=True)
    is_featured = models. BooleanField(default=False, verbose_name="Featured Event")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['-date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Auto-update status based on date
        if self.date < timezone.now().date() and self.status == 'upcoming':
            self.status = 'completed'
        super().save(*args, **kwargs)
    
    @property
    def is_past(self):
        return self.date < timezone.now().date()
    
    @property
    def is_upcoming(self):
        return self.date >= timezone.now().date()