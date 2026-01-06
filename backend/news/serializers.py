from rest_framework import serializers
from .models import NewsCategory, News

class NewsCategorySerializer(serializers.ModelSerializer):
    news_count = serializers.SerializerMethodField()
    
    class Meta:
        model = NewsCategory
        fields = '__all__'
    
    def get_news_count(self, obj):
        return obj.news_articles.filter(is_published=True).count()

class NewsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_url = serializers.SerializerMethodField()
    image_thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = '__all__'
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image. url) if request else obj.image.url
        return None
    
    def get_image_thumbnail_url(self, obj):
        if obj.image_thumbnail:
            request = self. context.get('request')
            return request.build_absolute_uri(obj.image_thumbnail.url) if request else obj.image_thumbnail.url
        return None

class NewsListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'excerpt', 'image_thumbnail_url', 
                  'category', 'category_name', 'author', 'date', 'is_featured']
    
    def get_image_thumbnail_url(self, obj):
        if obj.image_thumbnail:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image_thumbnail. url) if request else obj.image_thumbnail.url
        return None
