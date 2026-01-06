from django.contrib import admin
from .models import SiteSettings, HeroSlide, ContactInfo, QuickLink

@admin. register(SiteSettings)
class SiteSettingsAdmin(admin. ModelAdmin):
    list_display = ['site_name', 'contact_email', 'contact_phone', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_tagline', 'logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 
                      'linkedin_url', 'youtube_url', 'whatsapp_url', 'github_url'),
            'classes': ('collapse',)
        }),
        ('SEO & Analytics', {
            'fields':  ('meta_description', 'meta_keywords', 'google_analytics_id'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Allow only one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    list_editable = ['order', 'is_active']
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'image', 'image_alt')
        }),
        ('Buttons', {
            'fields': (
                ('button1_text', 'button1_url', 'button1_style'),
                ('button2_text', 'button2_url', 'button2_style')
            ),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )

@admin.register(ContactInfo)
class ContactInfoAdmin(admin. ModelAdmin):
    list_display = ['email', 'phone', 'updated_at']
    fieldsets = (
        ('Contact Details', {
            'fields': ('email', 'phone', 'address', 'office_hours', 'emergency_contact')
        }),
        ('Map Coordinates', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(QuickLink)
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'order', 'is_active', 'open_new_tab']
    list_filter = ['is_active', 'open_new_tab']
    search_fields = ['name', 'url']
    list_editable = ['order', 'is_active']