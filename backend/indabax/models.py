from django.db import models
from django.core.validators import FileExtensionValidator
from imagekit.models import ProcessedImageField, ImageSpecField
from django.utils import timezone



class LearningResource(models.Model):
    RESOURCE_TYPES = [
        ('video', 'YouTube Video'),
        ('doc', 'Google Doc'),
        ('slide', 'Slides'),
        ('link', 'Other Link'),
        ('file', 'File Upload'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES, default='link')
    url = models.URLField(blank=True, help_text="Link to resource (YouTube, Google Doc, etc.)")
    file = models.FileField(upload_to='indabax/resources/', blank=True, null=True)
    image = ProcessedImageField(
        upload_to='indabax/resources/images/',
        format='JPEG',
        options={'quality': 90},  # Optionally increase quality if you want even heavier!
        blank=True,
        null=True,
        help_text="Optional thumbnail/preview image"
    )
    uploaded_by = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Learning Resource"
        verbose_name_plural = "Learning Resources"
        ordering = ['-date_added']

    def __str__(self):
        return self.title

class HeroSection(models.Model):
    """Dynamic hero section for IndabaX"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = ProcessedImageField(
        upload_to='indabax/hero/',
        format='JPEG',
        options={'quality': 90},
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])],
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=False, help_text="Only one hero can be active.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

    def save(self, *args, **kwargs):
        if self.is_active:
            HeroSection.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Leader(models.Model):
    """Leader profile for IndabaX"""
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    profile_image = ProcessedImageField(
        upload_to='indabax/leaders/',
        format='JPEG',
        options={'quality': 90},
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])],
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)
    course = models.CharField(max_length=100, blank=True)
    start_year = models.PositiveIntegerField(default=timezone.now().year, help_text="Leadership start year")
    end_year = models.PositiveIntegerField(blank=True, null=True, help_text="Leadership end year; blank = current")
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    github = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Leader"
        verbose_name_plural = "Leaders"
        ordering = ['-start_year', '-end_year', 'name']

    def __str__(self):
        return f"{self.name} ({self.role})"

    @property
    def is_current(self):
        year = timezone.now().year
        return (self.end_year is None) or (self.end_year >= year)

    @property
    def is_archived(self):
        year = timezone.now().year
        return (self.end_year is not None and self.end_year < year)
from django.utils.text import slugify

class IndabaxSettings(models.Model):
    """Indabax site settings"""
    site_name = models.CharField(max_length=200, default="Indabax Kabale")
    tagline = models.CharField(max_length=500, blank=True)
    logo = ProcessedImageField(
        upload_to='indabax/logos/',
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
        format='JPEG',
        options={'quality': 85},
        blank=True,
        null=True
    )
    
    # Vision & Mission Section
    vision_title = models.CharField(max_length=200, default="Our Vision", blank=True)
    vision_description = models.TextField(blank=True)
    mission_title = models.CharField(max_length=200, default="Our Mission", blank=True)
    mission_description = models.TextField(blank=True)
    vision_mission_image = ProcessedImageField(
        upload_to='indabax/vision_mission/',
        format='JPEG',
        options={'quality': 85},
        blank=True,
        null=True,
        help_text="Optional image for Vision & Mission section"
    )
    
    # Contact
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
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
    registration_url = models.URLField(blank=True)
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
    is_active = models.BooleanField(default=True)
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
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sessions'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100, blank=True)
    
    # Materials
    slides_url = models.URLField(blank=True, verbose_name="Slides URL")
    video_url = models.URLField(blank=True, verbose_name="Recording URL")
    
    # Display
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Indabax Session"
        verbose_name_plural = "Indabax Sessions"
        ordering = ['date', 'start_time', 'order']
    
    def __str__(self):
        return f"{self.title} - {self.get_session_type_display()}"

class IndabaxGallery(models.Model):
    """Indabax gallery images"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Image
    image = ProcessedImageField(
        upload_to='indabax/gallery/',
        format='JPEG',
        options={'quality': 90},
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])]
    )
    
    image_thumbnail = ImageSpecField(
        source='image',
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