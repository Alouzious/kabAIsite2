from rest_framework import serializers
from .models import TeamRole, TeamMember

class TeamRoleSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TeamRole
        fields = '__all__'
    
    def get_members_count(self, obj):
        return obj.members.filter(is_active=True).count()

class TeamMemberSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    display_title = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()
    photo_thumbnail_url = serializers. SerializerMethodField()
    
    class Meta:
        model = TeamMember
        fields = '__all__'
    
    def get_display_title(self, obj):
        return obj.get_display_title()
    
    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return None
    
    def get_photo_thumbnail_url(self, obj):
        if obj.photo_thumbnail:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.photo_thumbnail.url) if request else obj. photo_thumbnail.url
        return None

class TeamMemberListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    role_name = serializers.CharField(source='role.name', read_only=True)
    display_title = serializers.SerializerMethodField()
    photo_thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'role_name', 'display_title', 'photo_thumbnail_url',
                  'linkedin_url', 'twitter_url', 'github_url', 'is_executive', 'order']
    
    def get_display_title(self, obj):
        return obj.get_display_title()
    
    def get_photo_thumbnail_url(self, obj):
        if obj.photo_thumbnail:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.photo_thumbnail.url) if request else obj.photo_thumbnail.url
        return None
