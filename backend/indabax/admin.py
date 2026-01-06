from django.contrib import admin
from .models import (
    IndabaxSettings, 
    IndabaxEvent, 
    IndabaxSpeaker, 
    IndabaxSession, 
    IndabaxGallery
)

@admin.register(IndabaxSettings)
class IndabaxSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_email', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields':  ('site_name', 'tagline', 'logo')
        }),
        ('About Section', {
            'fields': ('about_title', 'about_description', 'about_image')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'location')
        }),
        ('Social Media', {
            'fields':  ('facebook_url', 'twitter_url', 'instagram_url', 
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