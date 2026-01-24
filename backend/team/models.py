from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from django.core.validators import FileExtensionValidator
from django.utils import timezone

class TeamMember(models.Model):
    """Team members and leaders (no roles, auto-archiving for past members)"""
    name = models.CharField(max_length=200)
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Custom title/position (e.g. President, Secretary)"
    )
    bio = models.TextField(blank=True, help_text="Brief biography")
    
    # Photo
    photo = ProcessedImageField(
        upload_to='team/',
        processors=[ResizeToFill(400, 400)],  # Square for profile
        format='JPEG',
        options={'quality': 90},
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        help_text="Recommended: Square image (400x400px)"
    )
    photo_thumbnail = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(150, 150)],
        format='JPEG',
        options={'quality': 85}
    )
    
    # Contact & Social
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn Profile")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter/X Profile")
    github_url = models.URLField(blank=True, verbose_name="GitHub Profile")
    website_url = models.URLField(blank=True, verbose_name="Personal Website")
    
    # Leadership Years
    start_year = models.PositiveIntegerField(default=timezone.now().year, help_text="Leadership start year (e.g. 2024)")
    end_year = models.PositiveIntegerField(blank=True, null=True, help_text="Leadership end year; if blank, member is current")
    
    # Display Settings
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    is_active = models.BooleanField(default=True, verbose_name="Show on website")
    is_executive = models.BooleanField(default=False, verbose_name="Executive Team Member")
    
    joined_date = models.DateField(blank=True, null=True, help_text="Date joined KUAI or club")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['-start_year', '-end_year', 'order', 'name']  # Only use real DB fields for ordering

    def __str__(self):
        return f"{self.name} ({self.display_title})"

    @property
    def is_current(self):
        # If end_year not set, or is in the future, they are still current
        if self.end_year is None or self.end_year >= timezone.now().year:
            return True
        return False
    
    @property
    def display_title(self):
        return self.title if self.title else "Member"