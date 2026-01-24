from django.contrib import admin
from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_title', 'start_year', 'end_year', 'is_current', 'is_executive', 'is_active']
    list_filter = ['is_executive', 'is_active', 'start_year', 'end_year']
    search_fields = ['name', 'title', 'bio', 'email', 'linkedin_url', 'twitter_url', 'github_url']
    list_editable = ['is_executive', 'is_active']
    ordering = ['-start_year', '-end_year', 'order', 'name']  # <-- Fix: only use real fields, not 'is_current'
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'bio', 'photo')
        }),
        ('Contact & Social', {
            'fields': ('email', 'phone', 'linkedin_url', 'twitter_url', 'github_url', 'website_url'),
            'classes': ('collapse',)
        }),
        ('Leadership Years', {
            'fields': ('start_year', 'end_year', 'joined_date'),
        }),
        ('Display Settings', {
            'fields': ('is_executive', 'is_active', 'order')
        }),
    )

    def is_current(self, obj):
        return obj.is_current
    is_current.boolean = True