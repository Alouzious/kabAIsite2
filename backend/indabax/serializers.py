from rest_framework import serializers
from .models import (
    LearningResource,
    IndabaxSettings,
    IndabaxEvent,
    IndabaxSpeaker,
    IndabaxSession,
    IndabaxGallery,
    HeroSection,
    Leader,
)

class HeroSectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroSection
        fields = ['id', 'title', 'description', 'image_url', 'is_active', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class LearningResourceSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = LearningResource
        fields = [
            'id', 'title', 'description', 'resource_type', 'url', 'file_url', 
            'image_url', 'uploaded_by', 'date_added', 'is_published'
        ]

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class LeaderSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    is_current = serializers.SerializerMethodField()
    is_archived = serializers.SerializerMethodField()

    class Meta:
        model = Leader
        fields = [
            'id', 'name', 'role', 'profile_image_url', 'bio',
            'course', 'start_year', 'end_year',
            'is_current', 'is_archived',
            'linkedin', 'twitter', 'github', 'email',
            'created_at', 'updated_at',
        ]

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.profile_image.url) if request else obj.profile_image.url
        return None

    def get_is_current(self, obj):
        return obj.is_current

    def get_is_archived(self, obj):
        return obj.is_archived


class IndabaxSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    about_image_url = serializers.SerializerMethodField()
    vision_mission_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = IndabaxSettings
        fields = '__all__'
    
    def get_logo_url(self, obj):
        if obj.logo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
        return None
    
    def get_about_image_url(self, obj):
        if obj.about_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.about_image.url) if request else obj.about_image.url
        return None
    
    def get_vision_mission_image_url(self, obj):
        if obj.vision_mission_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.vision_mission_image.url) if request else obj.vision_mission_image.url
        return None

class IndabaxEventSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    speakers_count = serializers.SerializerMethodField()
    sessions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = IndabaxEvent
        fields = '__all__'
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
    
    def get_speakers_count(self, obj):
        return obj.speakers.filter(is_active=True).count()
    
    def get_sessions_count(self, obj):
        return obj.sessions.filter(is_active=True).count()

class IndabaxSpeakerSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = IndabaxSpeaker
        fields = '__all__'
    
    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return None

class IndabaxSessionSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    speaker_name = serializers.CharField(source='speaker.name', read_only=True)
    session_type_display = serializers.CharField(source='get_session_type_display', read_only=True)
    
    class Meta:
        model = IndabaxSession
        fields = '__all__'

class IndabaxGallerySerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    image_url = serializers.SerializerMethodField()
    image_thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = IndabaxGallery
        fields = '__all__'
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
    
    def get_image_thumbnail_url(self, obj):
        if obj.image_thumbnail:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image_thumbnail.url) if request else obj.image_thumbnail.url
        return None