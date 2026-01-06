from django.contrib import admin
from .models import About

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at']
    fieldsets = (
        ('Hero Section', {
            'fields':  ('title', 'content', 
                      ('hero_stat_1_value', 'hero_stat_1_label'),
                      ('hero_stat_2_value', 'hero_stat_2_label'),
                      ('hero_stat_3_value', 'hero_stat_3_label'),
                      ('hero_stat_4_value', 'hero_stat_4_label'))
        }),
        ('Who We Are', {
            'fields': ('who_we_are_title', 'who_we_are_description', 'who_we_are_image')
        }),
        ('Why We Exist', {
            'fields': ('why_exist_title', 'why_exist_description', 'image')
        }),
        ('Mission & Vision', {
            'fields': ('mission', 'vision')
        }),
        ('Impact Section', {
            'fields': ('impact_subtitle',
                      ('impact_stat_1_value', 'impact_stat_1_label'),
                      ('impact_stat_2_value', 'impact_stat_2_label'),
                      ('impact_stat_3_value', 'impact_stat_3_label'),
                      ('impact_stat_4_value', 'impact_stat_4_label')),
            'classes': ('collapse',)
        }),
        ('Call to Action', {
            'fields': ('cta_title', 'cta_description',
                      ('cta_primary_text', 'cta_primary_link'),
                      ('cta_secondary_text', 'cta_secondary_link')),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return not About.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False