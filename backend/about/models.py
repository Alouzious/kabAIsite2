from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.core.validators import FileExtensionValidator

class About(models.Model):
    """About page content"""
    # Hero Section
    title = models.CharField(max_length=200, default="About KUAI Club")
    content = models.TextField(help_text="Hero section description")
    
    # Hero Stats
    hero_stat_1_value = models.CharField(max_length=20, default="500+")
    hero_stat_1_label = models.CharField(max_length=50, default="Students")
    hero_stat_2_value = models.CharField(max_length=20, default="50+")
    hero_stat_2_label = models.CharField(max_length=50, default="Projects")
    hero_stat_3_value = models.CharField(max_length=20, default="15+")
    hero_stat_3_label = models.CharField(max_length=50, default="Partners")
    hero_stat_4_value = models.CharField(max_length=20, default="3")
    hero_stat_4_label = models.CharField(max_length=50, default="Years")
    
    # Who We Are Section
    who_we_are_title = models.CharField(max_length=200, default="Who We Are")
    who_we_are_description = models.TextField()
    who_we_are_image = ProcessedImageField(
        upload_to='about/',
        processors=[ResizeToFit(800, 600)],
        format='JPEG',
        options={'quality': 85},
        blank=True,
        null=True
    )
    
    # Why We Exist Section
    why_exist_title = models.CharField(max_length=200, default="Why We Exist")
    why_exist_description = models.TextField()
    image = ProcessedImageField(
        upload_to='about/',
        processors=[ResizeToFit(800, 600)],
        format='JPEG',
        options={'quality': 85},
        blank=True,
        null=True,
        verbose_name="Why We Exist Image"
    )
    
    # Mission & Vision
    mission = models.TextField(verbose_name="Our Mission")
    vision = models. TextField(verbose_name="Our Vision")
    
    # Impact Section
    impact_subtitle = models.CharField(max_length=500, blank=True)
    impact_stat_1_value = models.CharField(max_length=20, default="1000+")
    impact_stat_1_label = models.CharField(max_length=100, default="Students Empowered")
    impact_stat_2_value = models.CharField(max_length=20, default="75+")
    impact_stat_2_label = models.CharField(max_length=100, default="AI Projects Completed")
    impact_stat_3_value = models.CharField(max_length=20, default="25+")
    impact_stat_3_label = models.CharField(max_length=100, default="Partner Organizations")
    impact_stat_4_value = models.CharField(max_length=20, default="5")
    impact_stat_4_label = models.CharField(max_length=100, default="Years of Innovation")
    
    # Call to Action
    cta_title = models.CharField(max_length=200, default="Ready to Join the AI Revolution?")
    cta_description = models.TextField()
    cta_primary_text = models.CharField(max_length=50, default="Get Started Today")
    cta_primary_link = models.CharField(max_length=200, default="/")
    cta_secondary_text = models. CharField(max_length=50, default="Explore Programs")
    cta_secondary_link = models.CharField(max_length=200, default="/#projects-section")
    
    # Timestamps
    created_at = models. DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"
    
    def __str__(self):
        return self. title
    
    def save(self, *args, **kwargs):
        # Ensure only one About instance exists
        if not self.pk and About.objects.exists():
            raise ValueError('There can only be one About page instance')
        return super(About, self).save(*args, **kwargs)