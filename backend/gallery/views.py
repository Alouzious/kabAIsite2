from rest_framework import viewsets, filters
from rest_framework. decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from . models import GalleryCategory, GalleryImage
from .serializers import GalleryCategorySerializer, GalleryImageSerializer

class GalleryCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for gallery categories"""
    queryset = GalleryCategory.objects. filter(is_active=True)
    serializer_class = GalleryCategorySerializer

class GalleryImageViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for gallery images"""
    queryset = GalleryImage. objects.filter(is_active=True)
    serializer_class = GalleryImageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured', 'event_name']
    search_fields = ['title', 'description', 'tags', 'event_name']
    ordering_fields = ['order', 'date_taken', 'created_at']
    ordering = ['order', '-date_taken']
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured gallery images"""
        featured_images = self.get_queryset().filter(is_featured=True)[:12]
        serializer = self.get_serializer(featured_images, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get gallery images grouped by category"""
        categories = GalleryCategory. objects.filter(is_active=True)
        result = []
        
        for category in categories:
            images = self.get_queryset().filter(category=category)[:10]
            if images.exists():
                result. append({
                    'category':  GalleryCategorySerializer(category).data,
                    'images': GalleryImageSerializer(images, many=True, context={'request': request}).data
                })
        
        return Response(result)