from rest_framework import serializers
from .models import SiteSettings, HeroSlide, ContactInfo, QuickLink

class SiteSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    favicon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SiteSettings
        fields = '__all__'
    
    def get_logo_url(self, obj):
        try:
            if obj.logo:
                request = self.context.get('request')
                return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
        except Exception:
            return None
    
    def get_favicon_url(self, obj):
        try:
            if obj.favicon:
                request = self.context.get('request')
                return request.build_absolute_uri(obj.favicon.url) if request else obj.favicon.url
        except Exception:
            return None


class HeroSlideSerializer(serializers.ModelSerializer):
    # Safe image URL generation with fallbacks
    image_url = serializers.SerializerMethodField()
    image_desktop_url = serializers.SerializerMethodField()
    image_tablet_url = serializers.SerializerMethodField()
    image_mobile_url = serializers.SerializerMethodField()
    
    class Meta:
        model = HeroSlide
        fields = [
            'id', 'title', 'subtitle', 'image_alt',
            'image_url', 'image_desktop_url', 'image_tablet_url', 'image_mobile_url',
            'button1_text', 'button1_url', 'button1_style',
            'button2_text', 'button2_url', 'button2_style',
            'order', 'is_active'
        ]
    
    def get_image_url(self, obj):
        """Get the original image URL"""
        try:
            if obj.image:
                request = self.context.get('request')
                return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        except Exception as e:
            print(f"Error getting image URL: {e}")
            return None
    
    def get_image_desktop_url(self, obj):
        """Get desktop image with fallback to original"""
        try:
            if obj.image_desktop:
                request = self.context.get('request')
                return request.build_absolute_uri(obj.image_desktop.url) if request else obj.image_desktop.url
        except Exception as e:
            print(f"Error getting desktop image: {e}")
            # Fallback to original image
            return self.get_image_url(obj)
    
    def get_image_tablet_url(self, obj):
        """Get tablet image with fallback to original"""
        try:
            if obj.image_tablet:
                request = self.context.get('request')
                return request.build_absolute_uri(obj.image_tablet.url) if request else obj.image_tablet.url
        except Exception as e:
            print(f"Error getting tablet image: {e}")
            # Fallback to original image
            return self.get_image_url(obj)
    
    def get_image_mobile_url(self, obj):
        """Get mobile image with fallback to original"""
        try:
            if obj.image_mobile:
                request = self.context.get('request')
                return request.build_absolute_uri(obj.image_mobile.url) if request else obj.image_mobile.url
        except Exception as e:
            print(f"Error getting mobile image: {e}")
            # Fallback to original image
            return self.get_image_url(obj)


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = '__all__'


class QuickLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickLink
        fields = '__all__'