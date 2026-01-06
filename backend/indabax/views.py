from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    IndabaxSettings,
    IndabaxEvent,
    IndabaxSpeaker,
    IndabaxSession,
    IndabaxGallery
)
from .serializers import (
    IndabaxSettingsSerializer,
    IndabaxEventSerializer,
    IndabaxSpeakerSerializer,
    IndabaxSessionSerializer,
    IndabaxGallerySerializer
)

class IndabaxSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for Indabax settings"""
    queryset = IndabaxSettings.objects.all()
    serializer_class = IndabaxSettingsSerializer
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current Indabax settings"""
        try:
            settings = IndabaxSettings.objects.first()
            if settings:
                serializer = self.get_serializer(settings, context={'request': request})
                return Response(serializer.data)
            return Response({'detail':  'Indabax settings not configured yet.'}, status=404)
        except IndabaxSettings. DoesNotExist:
            return Response({'detail': 'Indabax settings not found.'}, status=404)

class IndabaxEventViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for Indabax events"""
    queryset = IndabaxEvent.objects.filter(is_published=True)
    serializer_class = IndabaxEventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_featured', 'date']
    search_fields = ['title', 'description', 'theme', 'location']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']
    lookup_field = 'slug'
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get the latest Indabax event"""
        latest_event = self.get_queryset().first()
        if latest_event: 
            serializer = self.get_serializer(latest_event, context={'request': request})
            return Response(serializer.data)
        return Response({'detail': 'No events found.'}, status=404)
    
    @action(detail=True, methods=['get'])
    def speakers(self, request, slug=None):
        """Get speakers for a specific event"""
        event = self.get_object()
        speakers = IndabaxSpeaker. objects.filter(event=event, is_active=True)
        serializer = IndabaxSpeakerSerializer(speakers, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def sessions(self, request, slug=None):
        """Get sessions for a specific event"""
        event = self.get_object()
        sessions = IndabaxSession.objects.filter(event=event, is_active=True)
        serializer = IndabaxSessionSerializer(sessions, many=True, context={'request': request})
        return Response(serializer.data)

class IndabaxSpeakerViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for Indabax speakers"""
    queryset = IndabaxSpeaker. objects.filter(is_active=True)
    serializer_class = IndabaxSpeakerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event', 'is_keynote']
    search_fields = ['name', 'title', 'organization', 'bio']
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']
    
    @action(detail=False, methods=['get'])
    def keynote(self, request):
        """Get keynote speakers"""
        keynote_speakers = self.get_queryset().filter(is_keynote=True)
        serializer = self.get_serializer(keynote_speakers, many=True, context={'request': request})
        return Response(serializer.data)

class IndabaxSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for Indabax sessions"""
    queryset = IndabaxSession. objects.filter(is_active=True)
    serializer_class = IndabaxSessionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event', 'session_type', 'speaker', 'date']
    search_fields = ['title', 'description', 'room']
    ordering_fields = ['date', 'start_time', 'order']
    ordering = ['date', 'start_time', 'order']

class IndabaxGalleryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for Indabax gallery"""
    queryset = IndabaxGallery.objects.filter(is_active=True)
    serializer_class = IndabaxGallerySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'date_taken', 'created_at']
    ordering = ['order', '-date_taken']