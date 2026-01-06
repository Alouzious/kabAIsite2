from django.contrib import admin
from . models import ProjectCategory, Project

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'color', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['icon', 'color', 'is_active']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'is_published', 'is_featured', 'order', 'created_at']
    list_filter = ['status', 'is_published', 'is_featured', 'category', 'start_date']
    search_fields = ['title', 'description', 'technologies', 'team_members']
    prepopulated_fields = {'slug':  ('title',)}
    list_editable = ['status', 'is_published', 'is_featured', 'order']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description', 'image')
        }),
        ('Project Details', {
            'fields': ('category', 'technologies', 'team_members', 
                      ('start_date', 'end_date'), 'status')
        }),
        ('Links', {
            'fields': ('github_url', 'demo_url', 'documentation_url'),
            'classes': ('collapse',)
        }),
        ('Publication & Display', {
            'fields': ('is_published', 'is_featured', 'order')
        }),
    )