from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify

class IndabaxSettings(models.Model):
    """Indabax site settings"""
    site_name = models.CharField(max_length=200, default="Indabax Kabale")
    tagline = models.CharField(max_length=500, blank=True)
    logo = ProcessedImageField(
        upload_to='indabax/logos/',
        processors=[ResizeToFit(300, 100)],
        format='PNG',
        options={'quality': 90},
        blank=True,
        null=True
    )
    
    # About Section
    about_title = models.CharField(max_length=200, default="About Indabax Kabale")
    about_description = models.TextField()
    about_image = ProcessedImageField(
        upload_to='indabax/about/',
        processors=[ResizeToFit(800, 600)],
        format='JPEG',
        options={'quality':  85},
        blank=True,
        null=True
    )
    
    # Contact
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models. URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Timestamps
    created_at = models. DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Indabax Settings"
        verbose_name_plural = "Indabax Settings"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        if not self.pk and IndabaxSettings.objects.exists():
            raise ValueError('There can only be one IndabaxSettings instance')
        return super(IndabaxSettings, self).save(*args, **kwargs)

class IndabaxEvent(models.Model):
    """Indabax events"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    theme = models.CharField(max_length=200, blank=True, help_text="Event theme")
    
    # Image
    image = ProcessedImageField(
        upload_to='indabax/events/',
        processors=[ResizeToFill(800, 600)],
        format='JPEG',
        options={'quality': 85},
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])]
    )
    
    # Event Details
    date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200)
    venue = models.CharField(max_length=200, blank=True)
    
    # Registration
    registration_url = models. URLField(blank=True)
    registration_deadline = models.DateField(blank=True, null=True)
    max_participants = models.IntegerField(blank=True, null=True)
    
    # Status
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Indabax Event"
        verbose_name_plural = "Indabax Events"
        ordering = ['-date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class IndabaxSpeaker(models.Model):
    """Indabax speakers"""
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, help_text="Professional title/position")
    organization = models.CharField(max_length=200, blank=True)
    bio = models.TextField()
    
    # Photo
    photo = ProcessedImageField(
        upload_to='indabax/speakers/',
        processors=[ResizeToFill(400, 400)],
        format='JPEG',
        options={'quality': 90},
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )
    
    # Event Association
    event = models.ForeignKey(
        IndabaxEvent,
        on_delete=models.CASCADE,
        related_name='speakers',
        blank=True,
        null=True
    )
    
    # Social Links
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    
    # Display
    order = models.IntegerField(default=0)
    is_active = models. BooleanField(default=True)
    is_keynote = models.BooleanField(default=False, verbose_name="Keynote Speaker")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta: 
        verbose_name = "Indabax Speaker"
        verbose_name_plural = "Indabax Speakers"
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.title}"

class IndabaxSession(models.Model):
    """Conference sessions/workshops"""
    SESSION_TYPES = [
        ('keynote', 'Keynote'),
        ('talk', 'Talk'),
        ('workshop', 'Workshop'),
        ('panel', 'Panel Discussion'),
        ('tutorial', 'Tutorial'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES, default='talk')
    
    # Session Details
    event = models.ForeignKey(
        IndabaxEvent,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    speaker = models.ForeignKey(
        IndabaxSpeaker,
        on_delete=models. SET_NULL,
        null=True,
        blank=True,
        related_name='sessions'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models. TimeField()
    room = models.CharField(max_length=100, blank=True)
    
    # Materials
    slides_url = models.URLField(blank=True, verbose_name="Slides URL")
    video_url = models.URLField(blank=True, verbose_name="Recording URL")
    
    # Display
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models. DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Indabax Session"
        verbose_name_plural = "Indabax Sessions"
        ordering = ['date', 'start_time', 'order']
    
    def __str__(self):
        return f"{self.title} - {self.get_session_type_display()}"

class IndabaxGallery(models.Model):
    """Indabax gallery images"""
    title = models. CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Image
    image = ProcessedImageField(
        upload_to='indabax/gallery/',
        processors=[ResizeToFit(1200, 900)],
        format='JPEG',
        options={'quality': 90},
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])]
    )
    
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality':  80}
    )
    
    # Event Association
    event = models.ForeignKey(
        IndabaxEvent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='gallery_images'
    )
    
    # Display
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    date_taken = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Indabax Gallery Image"
        verbose_name_plural = "Indabax Gallery Images"
        ordering = ['order', '-date_taken']
    
    def __str__(self):
        return self.title