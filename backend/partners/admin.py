from django.contrib import admin
from .models import PartnerCategory, Partner

@admin.register(PartnerCategory)
class PartnerCategoryAdmin(admin. ModelAdmin):
    list_display = ['name', 'category_type', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'category_type']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'partnership_level', 'is_featured', 'is_active', 'order', 'partnership_since']
    list_filter = ['is_active', 'is_featured', 'category', 'partnership_since']
    search_fields = ['name', 'description', 'partnership_level']
    list_editable = ['is_featured', 'is_active', 'order']
    date_hierarchy = 'partnership_since'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'logo', 'category')
        }),
        ('Partnership Details', {
            'fields': ('partnership_level', 'partnership_since', 'website_url')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active', 'is_featured')
        }),
    )