from rest_framework import viewsets, filters
from rest_framework. decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from . models import ProjectCategory, Project
from .serializers import ProjectCategorySerializer, ProjectSerializer, ProjectListSerializer

class ProjectCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for project categories"""
    queryset = ProjectCategory.objects.filter(is_active=True)
    serializer_class = ProjectCategorySerializer
    lookup_field = 'slug'

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for projects"""
    queryset = Project. objects.filter(is_published=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'is_featured']
    search_fields = ['title', 'description', 'technologies', 'team_members']
    ordering_fields = ['order', 'created_at', 'title']
    ordering = ['order', '-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list': 
            return ProjectListSerializer
        return ProjectSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured projects"""
        featured_projects = self.get_queryset().filter(is_featured=True)[: 6]
        serializer = ProjectListSerializer(featured_projects, many=True, context={'request': request})
        return Response(serializer. data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get projects grouped by status"""
        statuses = ['completed', 'in_progress', 'planning']
        result = {}
        
        for status in statuses:
            projects = self.get_queryset().filter(status=status)[:10]
            result[status] = ProjectListSerializer(projects, many=True, context={'request': request}).data
        
        return Response(result)