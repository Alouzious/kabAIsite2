from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import EventCategory, Event
from .serializers import EventCategorySerializer, EventSerializer, EventListSerializer

class EventCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for event categories"""
    queryset = EventCategory.objects.filter(is_active=True)
    serializer_class = EventCategorySerializer
    lookup_field = 'slug'

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for events"""
    queryset = Event.objects.filter(is_published=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'is_featured', 'date']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date', 'created_at', 'title']
    ordering = ['-date']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        return EventSerializer
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming events"""
        upcoming_events = self.get_queryset().filter(
            date__gte=timezone.now().date(),
            status='upcoming'
        ).order_by('date')
        
        page = self.paginate_queryset(upcoming_events)
        if page is not None:
            serializer = EventListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = EventListSerializer(upcoming_events, many=True, context={'request': request})
        return Response(serializer. data)
    
    @action(detail=False, methods=['get'])
    def past(self, request):
        """Get past events"""
        past_events = self.get_queryset().filter(
            date__lt=timezone.now().date()
        ).order_by('-date')
        
        page = self.paginate_queryset(past_events)
        if page is not None:
            serializer = EventListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer. data)
        
        serializer = EventListSerializer(past_events, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured events"""
        featured_events = self.get_queryset().filter(is_featured=True).order_by('-date')[:6]
        serializer = EventListSerializer(featured_events, many=True, context={'request': request})
        return Response(serializer.data)