from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from . models import NewsCategory, News
from .serializers import NewsCategorySerializer, NewsSerializer, NewsListSerializer

class NewsCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for news categories"""
    queryset = NewsCategory.objects.filter(is_active=True)
    serializer_class = NewsCategorySerializer
    lookup_field = 'slug'

class NewsViewSet(viewsets. ReadOnlyModelViewSet):
    """API endpoint for news articles"""
    queryset = News. objects.filter(is_published=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured', 'date']
    search_fields = ['title', 'excerpt', 'content', 'author']
    ordering_fields = ['date', 'created_at', 'title']
    ordering = ['-date', '-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NewsListSerializer
        return NewsSerializer