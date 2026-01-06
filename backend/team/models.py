from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from django.core.validators import FileExtensionValidator

class TeamRole(models.Model):
    """Team member roles/positions"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    
    created_at = models. DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Team Role"
        verbose_name_plural = "Team Roles"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class TeamMember(models.Model):
    """Team members and leaders"""
    name = models.CharField(max_length=200)
    role = models.ForeignKey(
        TeamRole,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Custom title/position (overrides role if provided)"
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
    
    # Display Settings
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    is_active = models.BooleanField(default=True, verbose_name="Show on website")
    is_executive = models.BooleanField(default=False, verbose_name="Executive Team Member")
    
    # Timestamps
    joined_date = models.DateField(blank=True, null=True, help_text="Date joined KUAI")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.get_display_title()}"
    
    def get_display_title(self):
        """Return custom title or role name"""
        return self.title if self.title else (self.role.name if self.role else "Member")