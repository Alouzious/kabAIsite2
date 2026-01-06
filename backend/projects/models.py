from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify

class ProjectCategory(models.Model):
    """Project categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    color = models.CharField(max_length=7, default="#007bff", help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    
    created_at = models. DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Project(models.Model):
    """AI Projects showcase"""
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Brief description for cards"
    )
    
    # Image
    image = ProcessedImageField(
        upload_to='projects/',
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
    
    # Project Details
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models. SET_NULL,
        null=True,
        blank=True,
        related_name='projects'
    )
    technologies = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated list (e.g., Python, TensorFlow, React)"
    )
    team_members = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated team member names"
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models. DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    
    # Links
    github_url = models.URLField(blank=True, verbose_name="GitHub Repository")
    demo_url = models.URLField(blank=True, verbose_name="Live Demo URL")
    documentation_url = models.URLField(blank=True, verbose_name="Documentation URL")
    
    # Publication
    is_published = models. BooleanField(default=True)
    is_featured = models. BooleanField(default=False, verbose_name="Featured Project")
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    
    # Timestamps
    created_at = models. DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.short_description:
            self.short_description = self.description[:197] + "..."
        super().save(*args, **kwargs)
    
    def get_technologies_list(self):
        """Return technologies as a list"""
        return [tech.strip() for tech in self.technologies. split(',')] if self.technologies else []
    
    def get_team_members_list(self):
        """Return team members as a list"""
        return [member.strip() for member in self.team_members.split(',')] if self.team_members else []