from rest_framework import serializers
from .models import SiteSettings, HeroSlide, ContactInfo, QuickLink

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'

class HeroSlideSerializer(serializers.ModelSerializer):
    # Generate different image sizes URLs
    image_desktop_url = serializers.SerializerMethodField()
    image_tablet_url = serializers.SerializerMethodField()
    image_mobile_url = serializers.SerializerMethodField()
    
    class Meta:
        model = HeroSlide
        fields = '__all__'
    
    def get_image_desktop_url(self, obj):
        if obj.image_desktop:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image_desktop.url) if request else obj.image_desktop.url
        return None
    
    def get_image_tablet_url(self, obj):
        if obj.image_tablet:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image_tablet.url) if request else obj. image_tablet.url
        return None
    
    def get_image_mobile_url(self, obj):
        if obj.image_mobile:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image_mobile. url) if request else obj.image_mobile.url
        return None

class ContactInfoSerializer(serializers. ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = '__all__'

class QuickLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickLink
        fields = '__all__'
