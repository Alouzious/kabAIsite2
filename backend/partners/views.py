from rest_framework import viewsets, filters
from rest_framework. decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from . models import PartnerCategory, Partner
from .serializers import PartnerCategorySerializer, PartnerSerializer

class PartnerCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for partner categories"""
    queryset = PartnerCategory.objects. filter(is_active=True)
    serializer_class = PartnerCategorySerializer

class PartnerViewSet(viewsets. ReadOnlyModelViewSet):
    """API endpoint for partners"""
    queryset = Partner.objects. filter(is_active=True)
    serializer_class = PartnerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name', 'description', 'partnership_level']
    ordering_fields = ['order', 'name', 'partnership_since']
    ordering = ['order', 'name']
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured partners"""
        featured_partners = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_partners, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get partners grouped by category"""
        categories = PartnerCategory.objects.filter(is_active=True)
        result = []
        
        for category in categories: 
            partners = self.get_queryset().filter(category=category)
            if partners.exists():
                result.append({
                    'category': PartnerCategorySerializer(category).data,
                    'partners': PartnerSerializer(partners, many=True, context={'request': request}).data
                })
        
        return Response(result)