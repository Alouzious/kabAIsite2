from .models import LearningResource
from .serializers import LearningResourceSerializer
from rest_framework import generics, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import (
    IndabaxSettings,
    IndabaxEvent,
    IndabaxSpeaker,
    IndabaxSession,
    IndabaxGallery,
    HeroSection,
    Leader
)
from .serializers import (
    IndabaxSettingsSerializer,
    IndabaxEventSerializer,
    IndabaxSpeakerSerializer,
    IndabaxSessionSerializer,
    IndabaxGallerySerializer,
    HeroSectionSerializer,
    LeaderSerializer
)
from django.views.generic import TemplateView
from django.shortcuts import render

class LearningResourceListView(generics.ListAPIView):
    queryset = LearningResource.objects.filter(is_published=True)
    serializer_class = LearningResourceSerializer

# IndabaX main page view (unchanged)
def indabax_main(request):
    hero = HeroSection.objects.filter(is_active=True).first()
    current_leaders = Leader.objects.filter(end_year__isnull=True) | Leader.objects.filter(end_year__gte=timezone.now().year)
    current_leaders = current_leaders.order_by('-start_year', '-end_year', 'name')
    context = {
        'hero': hero,
        'current_leaders': current_leaders,
    }
    return render(request, 'indabax/main.html', context)

def indabax_leaders(request):
    current_leaders = Leader.objects.filter(end_year__isnull=True) | Leader.objects.filter(end_year__gte=timezone.now().year)
    current_leaders = current_leaders.order_by('-start_year', '-end_year', 'name')
    archived_leaders = {}
    for year in Leader.objects.values_list('start_year', flat=True).distinct().order_by('-start_year'):
        archived = Leader.objects.filter(start_year=year, end_year__lt=timezone.now().year).order_by('name')
        if archived.exists():
            archived_leaders[year] = archived
    context = {
        'current_leaders': current_leaders,
        'archived_leaders': archived_leaders,
    }
    return render(request, 'indabax/leaders.html', context)

# API views for hero and leaders
class HeroSectionListView(generics.ListAPIView):
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer

# ----- ARCHIVE-COMPATIBLE LEADER API -----
class LeaderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for leaders (current and archived)
    """
    queryset = Leader.objects.all()
    serializer_class = LeaderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'role', 'bio', 'course']
    filterset_fields = ['role', 'start_year', 'end_year']
    ordering_fields = ['start_year', 'end_year', 'name', 'created_at']
    ordering = ['-start_year', '-end_year', 'name']

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current leaders only"""
        year = timezone.now().year
        leaders = Leader.objects.filter(end_year__isnull=True) | Leader.objects.filter(end_year__gte=year)
        leaders = leaders.distinct().order_by('-start_year', '-end_year', 'name')
        serializer = self.get_serializer(leaders, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def archived(self, request):
        """Get archived leaders (past years only)"""
        year = timezone.now().year
        leaders = Leader.objects.filter(end_year__lt=year)
        serializer = self.get_serializer(leaders, many=True, context={'request': request})
        return Response(serializer.data)

# --------------------------------------------------

class IndabaxSettingsViewSet(viewsets.ReadOnlyModelViewSet):
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
        except IndabaxSettings.DoesNotExist:
            return Response({'detail': 'Indabax settings not found.'}, status=404)

class IndabaxEventViewSet(viewsets.ReadOnlyModelViewSet):
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
        event = self.get_object()
        speakers = IndabaxSpeaker.objects.filter(event=event, is_active=True)
        serializer = IndabaxSpeakerSerializer(speakers, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def sessions(self, request, slug=None):
        event = self.get_object()
        sessions = IndabaxSession.objects.filter(event=event, is_active=True)
        serializer = IndabaxSessionSerializer(sessions, many=True, context={'request': request})
        return Response(serializer.data)

class IndabaxSpeakerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndabaxSpeaker.objects.filter(is_active=True)
    serializer_class = IndabaxSpeakerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event', 'is_keynote']
    search_fields = ['name', 'title', 'organization', 'bio']
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']
    
    @action(detail=False, methods=['get'])
    def keynote(self, request):
        keynote_speakers = self.get_queryset().filter(is_keynote=True)
        serializer = self.get_serializer(keynote_speakers, many=True, context={'request': request})
        return Response(serializer.data)

class IndabaxSessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndabaxSession.objects.filter(is_active=True)
    serializer_class = IndabaxSessionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event', 'session_type', 'speaker', 'date']
    search_fields = ['title', 'description', 'room']
    ordering_fields = ['date', 'start_time', 'order']
    ordering = ['date', 'start_time', 'order']

class IndabaxGalleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndabaxGallery.objects.filter(is_active=True)
    serializer_class = IndabaxGallerySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'date_taken', 'created_at']
    ordering = ['order', '-date_taken']