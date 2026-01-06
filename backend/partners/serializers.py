from rest_framework import serializers
from .models import PartnerCategory, Partner

class PartnerCategorySerializer(serializers. ModelSerializer):
    partners_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PartnerCategory
        fields = '__all__'
    
    def get_partners_count(self, obj):
        return obj.partners.filter(is_active=True).count()

class PartnerSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_type = serializers.CharField(source='category.category_type', read_only=True)
    logo_url = serializers.SerializerMethodField()
    logo_thumbnail_url = serializers. SerializerMethodField()
    
    class Meta:
        model = Partner
        fields = '__all__'
    
    def get_logo_url(self, obj):
        if obj.logo:
            request = self.context. get('request')
            return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
        return None
    
    def get_logo_thumbnail_url(self, obj):
        if obj.logo_thumbnail:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.logo_thumbnail. url) if request else obj.logo_thumbnail.url
        return None

