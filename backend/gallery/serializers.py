from rest_framework import serializers
from .models import GalleryCategory, GalleryImage

class GalleryCategorySerializer(serializers. ModelSerializer):
    images_count = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryCategory
        fields = '__all__'
    
    def get_images_count(self, obj):
        return obj.images.filter(is_active=True).count()

class GalleryImageSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_url = serializers. SerializerMethodField()
    image_thumbnail_url = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryImage
        fields = '__all__'
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context. get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
    
    def get_image_thumbnail_url(self, obj):
        if obj.image_thumbnail:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image_thumbnail. url) if request else obj.image_thumbnail.url
        return None
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()
