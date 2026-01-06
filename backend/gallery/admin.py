from django.contrib import admin
from .models import GalleryCategory, GalleryImage

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'event_name', 'date_taken', 'is_featured', 'is_active', 'order']
    list_filter = ['is_active', 'is_featured', 'category', 'date_taken']
    search_fields = ['title', 'description', 'event_name', 'photographer', 'tags']
    list_editable = ['is_featured', 'is_active', 'order']
    date_hierarchy = 'date_taken'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image', 'category')
        }),
        ('Metadata', {
            'fields':  ('photographer', 'event_name', 'date_taken', 'tags'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active', 'is_featured')
        }),
    )