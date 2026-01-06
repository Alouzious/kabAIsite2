from django.contrib import admin
from .models import TeamRole, TeamMember

@admin.register(TeamRole)
class TeamRoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'title', 'order', 'is_executive', 'is_active', 'joined_date']
    list_filter = ['is_active', 'is_executive', 'role', 'joined_date']
    search_fields = ['name', 'title', 'bio', 'email']
    list_editable = ['order', 'is_executive', 'is_active']
    date_hierarchy = 'joined_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'role', 'title', 'bio', 'photo')
        }),
        ('Contact Information', {
            'fields':  ('email', 'phone'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields':  ('linkedin_url', 'twitter_url', 'github_url', 'website_url'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active', 'is_executive', 'joined_date')
        }),
    )