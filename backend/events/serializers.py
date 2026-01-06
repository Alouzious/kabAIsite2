from rest_framework import serializers
from .models import EventCategory, Event

class EventCategorySerializer(serializers.ModelSerializer):
    events_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EventCategory
        fields = '__all__'
    
    def get_events_count(self, obj):
        return obj. events.filter(is_published=True).count()

class EventSerializer(serializers.ModelSerializer):
    category_name = serializers. CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    image_url = serializers.SerializerMethodField()
    image_thumbnail_url = serializers.SerializerMethodField()
    is_past = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
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

class EventListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_thumbnail_url = serializers.SerializerMethodField()
    is_past = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    
    class Meta: 
        model = Event
        fields = ['id', 'title', 'slug', 'image_thumbnail_url', 'category', 
                  'category_name', 'date', 'time', 'location', 'status', 
                  'is_featured', 'is_past', 'is_upcoming']
    
    def get_image_thumbnail_url(self, obj):
        if obj.image_thumbnail:
            request = self.context.get('request')
            return request. build_absolute_uri(obj. image_thumbnail.url) if request else obj.image_thumbnail.url
        return None
