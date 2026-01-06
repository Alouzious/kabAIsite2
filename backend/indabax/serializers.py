from rest_framework import serializers
from .models import (
    IndabaxSettings,
    IndabaxEvent,
    IndabaxSpeaker,
    IndabaxSession,
    IndabaxGallery
)

class IndabaxSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    about_image_url = serializers.SerializerMethodField()
    
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
            return request.build_absolute_uri(obj.about_image.url) if request else obj. about_image.url
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
            request = self. context.get('request')
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
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo. url
        return None

class IndabaxSessionSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    speaker_name = serializers.CharField(source='speaker.name', read_only=True)
    session_type_display = serializers.CharField(source='get_session_type_display', read_only=True)
    
    class Meta:
        model = IndabaxSession
        fields = '__all__'

class IndabaxGallerySerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event. title', read_only=True)
    image_url = serializers.SerializerMethodField()
    image_thumbnail_url = serializers. SerializerMethodField()
    
    class Meta:
        model = IndabaxGallery
        fields = '__all__'
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image. url) if request else obj.image.url
        return None
    
    def get_image_thumbnail_url(self, obj):
        if obj.image_thumbnail:
            request = self.context. get('request')
            return request.build_absolute_uri(obj.image_thumbnail.url) if request else obj.image_thumbnail. url
        return None
