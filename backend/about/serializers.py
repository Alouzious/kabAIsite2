from rest_framework import serializers
from .models import About

class AboutSerializer(serializers.ModelSerializer):
    who_we_are_image_url = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = About
        fields = '__all__'
    
    def get_who_we_are_image_url(self, obj):
        if obj.who_we_are_image: 
            request = self.context.get('request')
            return request.build_absolute_uri(obj.who_we_are_image.url) if request else obj.who_we_are_image.url
        return None
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image. url
        return None
