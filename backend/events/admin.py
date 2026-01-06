from django.contrib import admin
from .models import EventCategory, Event

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'color', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['icon', 'color', 'is_active']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'time', 'location', 'status', 'is_published', 'is_featured']
    list_filter = ['status', 'is_published', 'is_featured', 'category', 'date']
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'
    list_editable = ['status', 'is_published', 'is_featured']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'image', 'category')
        }),
        ('Event Details', {
            'fields': (('date', 'time'), 'end_date', 'location', 'venue_details')
        }),
        ('Registration', {
            'fields': ('registration_link', 'registration_deadline', 'max_participants'),
            'classes': ('collapse',)
        }),
        ('Status & Publication', {
            'fields': ('status', 'is_published', 'is_featured')
        }),
    )