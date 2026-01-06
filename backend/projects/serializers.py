from rest_framework import serializers
from .models import ProjectCategory, Project

class ProjectCategorySerializer(serializers.ModelSerializer):
    projects_count = serializers.SerializerMethodField()
    
    class Meta: 
        model = ProjectCategory
        fields = '__all__'
    
    def get_projects_count(self, obj):
        return obj.projects.filter(is_published=True).count()

class ProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    image_url = serializers.SerializerMethodField()
    image_thumbnail_url = serializers.SerializerMethodField()
    technologies_list = serializers.SerializerMethodField()
    team_members_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
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
    
    def get_technologies_list(self, obj):
        return obj.get_technologies_list()
    
    def get_team_members_list(self, obj):
        return obj.get_team_members_list()

class ProjectListSerializer(serializers. ModelSerializer):
    """Simplified serializer for list views"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_thumbnail_url = serializers. SerializerMethodField()
    technologies_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'short_description', 'image_thumbnail_url',
                  'category', 'category_name', 'technologies_list', 'status', 
                  'is_featured', 'github_url', 'demo_url']
    
    def get_image_thumbnail_url(self, obj):
        if obj.image_thumbnail:
            request = self. context.get('request')
            return request.build_absolute_uri(obj.image_thumbnail.url) if request else obj.image_thumbnail.url
        return None
    
    def get_technologies_list(self, obj):
        return obj.get_technologies_list()
