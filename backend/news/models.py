from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.core. validators import FileExtensionValidator
from django.utils.text import slugify

class NewsCategory(models.Model):
    """News categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self. name)
        super().save(*args, **kwargs)

class News(models.Model):
    """News articles"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=300, help_text="Brief summary (max 300 chars)")
    content = models.TextField(help_text="Full article content")
    
    # Image
    image = ProcessedImageField(
        upload_to='news/',
        processors=[ResizeToFill(800, 600)],
        format='JPEG',
        options={'quality': 85},
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
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news_articles'
    )
    author = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    is_published = models.BooleanField(default=True, verbose_name="Published")
    is_featured = models.BooleanField(default=False, verbose_name="Featured Article")
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models. DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self. slug = slugify(self.title)
        super().save(*args, **kwargs)