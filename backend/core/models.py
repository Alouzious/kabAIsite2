from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit. processors import ResizeToFill, ResizeToFit
from django.core.validators import FileExtensionValidator

class SiteSettings(models.Model):
    """Global site settings with optimized images"""
    site_name = models.CharField(max_length=200, default="KUAI Club")
    site_tagline = models.CharField(max_length=500, blank=True)
    
    # Logo with automatic resizing
    logo = ProcessedImageField(
        upload_to='logos/',
        processors=[ResizeToFit(300, 100)],  # Max width 300px, height 100px
        format='PNG',
        options={'quality': 90},
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])],
        help_text="Logo will be resized to fit 300x100px"
    )
    
    # Favicon with automatic resizing
    favicon = ProcessedImageField(
        upload_to='logos/',
        processors=[ResizeToFill(32, 32)],  # Exact 32x32px
        format='PNG',
        options={'quality': 90},
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['png', 'ico'])],
        help_text="Favicon will be resized to 32x32px"
    )
    
    # Contact Information
    contact_email = models.EmailField(blank=True)
    contact_phone = models. CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True, verbose_name="Facebook URL")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter/X URL")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram URL")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn URL")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube URL")
    whatsapp_url = models.URLField(blank=True, verbose_name="WhatsApp URL")
    github_url = models.URLField(blank=True, verbose_name="GitHub URL")
    
    # SEO
    meta_description = models.TextField(
        blank=True,
        max_length=160,
        help_text="Max 160 characters for SEO"
    )
    meta_keywords = models.TextField(
        blank=True,
        help_text="Comma-separated keywords"
    )
    
    # Analytics
    google_analytics_id = models.CharField(max_length=50, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models. DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one SiteSettings instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('There can only be one SiteSettings instance')
        return super(SiteSettings, self).save(*args, **kwargs)


class HeroSlide(models. Model):
    """Hero carousel slides with optimized images"""
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True, max_length=500)
    
    # Original image
    image = models.ImageField(
        upload_to='hero/',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])],
        help_text="Recommended size: 1920x1080px"
    )
    
    # Automatically generate optimized versions
    image_desktop = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1920, 1080)],
        format='JPEG',
        options={'quality':  85}
    )
    
    image_tablet = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1024, 768)],
        format='JPEG',
        options={'quality': 85}
    )
    
    image_mobile = ImageSpecField(
        source='image',
        processors=[ResizeToFill(768, 576)],
        format='JPEG',
        options={'quality': 80}
    )
    
    # Image alt text for accessibility
    image_alt = models.CharField(
        max_length=200,
        blank=True,
        help_text="Describe the image for accessibility"
    )
    
    # Buttons
    button1_text = models. CharField(max_length=50, blank=True)
    button1_url = models.CharField(max_length=200, blank=True)
    button1_style = models.CharField(
        max_length=50,
        default='primary',
        choices=[
            ('primary', 'Primary'),
            ('secondary', 'Secondary'),
            ('success', 'Success'),
            ('danger', 'Danger'),
            ('warning', 'Warning'),
            ('info', 'Info'),
            ('light', 'Light'),
            ('dark', 'Dark'),
        ]
    )
    
    button2_text = models.CharField(max_length=50, blank=True)
    button2_url = models.CharField(max_length=200, blank=True)
    button2_style = models.CharField(
        max_length=50,
        default='outline-light',
        choices=[
            ('outline-primary', 'Outline Primary'),
            ('outline-secondary', 'Outline Secondary'),
            ('outline-light', 'Outline Light'),
            ('outline-dark', 'Outline Dark'),
        ]
    )
    
    # Order and status
    order = models.IntegerField(
        default=0,
        help_text="Lower numbers appear first"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this slide"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models. DateTimeField(auto_now=True)
    
    class Meta: 
        ordering = ['order', '-created_at']
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"
    
    def __str__(self):
        return self.title


class ContactInfo(models.Model):
    """Contact information"""
    email = models.EmailField(help_text="Primary contact email")
    phone = models. CharField(
        max_length=20,
        help_text="Phone number with country code (e.g., +256)"
    )
    address = models.TextField(help_text="Physical address")
    office_hours = models.CharField(
        max_length=200,
        blank=True,
        help_text="e.g., Mon-Fri:  9AM-5PM"
    )
    
    # Map coordinates for embedding
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Latitude coordinate for map"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Longitude coordinate for map"
    )
    
    # Additional info
    emergency_contact = models.CharField(
        max_length=20,
        blank=True,
        help_text="Emergency contact number"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"
    
    def __str__(self):
        return f"Contact Info - {self.email}"
    
    def save(self, *args, **kwargs):
        # Ensure only one ContactInfo instance exists
        if not self.pk and ContactInfo.objects.exists():
            raise ValueError('There can only be one ContactInfo instance')
        return super(ContactInfo, self).save(*args, **kwargs)


class QuickLink(models.Model):
    """Quick links for top navigation"""
    name = models.CharField(max_length=100)
    url = models.URLField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    open_new_tab = models.BooleanField(
        default=True,
        help_text="Open link in new tab"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Quick Link"
        verbose_name_plural = "Quick Links"
    
    def __str__(self):
        return self. name