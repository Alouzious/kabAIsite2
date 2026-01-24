
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    IndabaxSettings, 
    IndabaxEvent, 
    IndabaxSpeaker, 
    IndabaxSession, 
    IndabaxGallery,
    HeroSection,
    Leader,
    LearningResource
)

# LearningResource admin
@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'uploaded_by', 'date_added', 'is_published', 'resource_image_preview']
    list_filter = ['resource_type', 'is_published', 'date_added']
    search_fields = ['title', 'description', 'uploaded_by']
    list_editable = ['is_published']
    readonly_fields = ['resource_image_preview']
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'resource_type', 'url', 'file', 'image', 'resource_image_preview', 'uploaded_by', 'is_published')
        }),
    )
    
    def resource_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:300px; max-height:200px; border-radius:8px;" />', obj.image.url)
        return "No image"
    resource_image_preview.short_description = "Image Preview"

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at', 'hero_image_preview']
    list_editable = ['is_active']
    readonly_fields = ['hero_image_preview']
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'is_active', 'hero_image_preview')
        }),
    )

    def hero_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:400px; max-height:200px;" />', obj.image.url)
        return "No image"
    hero_image_preview.short_description = "Image Preview"

from django.contrib import admin
from django.utils.html import format_html
from .models import Leader

@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'start_year', 'end_year', 'is_current_display', 'leader_image_preview']
    list_filter = ['start_year', 'end_year']
    search_fields = ['name', 'role', 'bio', 'course']
    readonly_fields = ['leader_image_preview']
    fieldsets = (
        (None, {
            'fields': (
                'name', 'role', 'profile_image', 'leader_image_preview', 'bio', 'course',
                'start_year', 'end_year',
                'linkedin', 'twitter', 'github', 'email'
            )
        }),
    )

    def leader_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="max-width:120px; max-height:120px; border-radius:50%;" />', obj.profile_image.url)
        return "No image"
    leader_image_preview.short_description = "Profile Preview"

    def is_current_display(self, obj):
        return obj.is_current
    is_current_display.short_description = 'Is Current?'
    is_current_display.boolean = True
    
@admin.register(IndabaxSettings)
class IndabaxSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_email', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'tagline', 'logo')
        }),
        ('About Section', {
            'fields': ('about_title', 'about_description', 'about_image')
        }),
        ('Vision & Mission', {
            'fields': ('vision_title', 'vision_description', 
                      'mission_title', 'mission_description', 
                      'vision_mission_image'),
            'classes': ('collapse',),
            'description': 'Optional: Add your organization\'s vision and mission statements'
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'location')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 
                      'linkedin_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return not IndabaxSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(IndabaxEvent)
class IndabaxEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'end_date', 'location', 'is_published', 'is_featured', 'created_at']
    list_filter = ['is_published', 'is_featured', 'date']
    search_fields = ['title', 'description', 'theme', 'location']
    prepopulated_fields = {'slug':  ('title',)}
    list_editable = ['is_published', 'is_featured']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'theme', 'image')
        }),
        ('Event Details', {
            'fields':  (('date', 'end_date'), 'time', 'location', 'venue')
        }),
        ('Registration', {
            'fields': ('registration_url', 'registration_deadline', 'max_participants'),
            'classes': ('collapse',)
        }),
        ('Publication', {
            'fields': ('is_published', 'is_featured')
        }),
    )

@admin.register(IndabaxSpeaker)
class IndabaxSpeakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'organization', 'event', 'is_keynote', 'is_active', 'order']
    list_filter = ['is_active', 'is_keynote', 'event']
    search_fields = ['name', 'title', 'organization', 'bio']
    list_editable = ['is_keynote', 'is_active', 'order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'organization', 'bio', 'photo')
        }),
        ('Event Association', {
            'fields':  ('event',)
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'twitter_url', 'website_url'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields':  ('order', 'is_active', 'is_keynote')
        }),
    )

@admin.register(IndabaxSession)
class IndabaxSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'session_type', 'event', 'speaker', 'date', 'start_time', 'end_time', 'room', 'is_active']
    list_filter = ['is_active', 'session_type', 'event', 'date']
    search_fields = ['title', 'description', 'room']
    list_editable = ['is_active']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'session_type')
        }),
        ('Session Details', {
            'fields': ('event', 'speaker', 'date', ('start_time', 'end_time'), 'room')
        }),
        ('Materials', {
            'fields': ('slides_url', 'video_url'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )

@admin.register(IndabaxGallery)
class IndabaxGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'date_taken', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'event', 'date_taken']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'order']
    date_hierarchy = 'date_taken'
    
    fieldsets = (
        ('Basic Information', {
            'fields':  ('title', 'description', 'image')
        }),
        ('Event Association', {
            'fields': ('event',)
        }),
        ('Display Settings', {
            'fields': ('date_taken', 'order', 'is_active')
        }),
    )