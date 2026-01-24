from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .models import TeamMember
from .serializers import TeamMemberSerializer

class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for all team members (current and past/archived) with FULL info"""
    queryset = TeamMember.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_executive', 'start_year', 'end_year']
    search_fields = ['name', 'title', 'bio']
    ordering_fields = ['order', 'name', 'start_year', 'end_year']
    ordering = ['-start_year', '-end_year', 'order', 'name']

    def get_serializer_class(self):
        # Always use full serializer
        return TeamMemberSerializer

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current team members"""
        now_year = timezone.now().year
        members = self.get_queryset().filter(
            end_year__isnull=True
        ) | self.get_queryset().filter(end_year__gte=now_year)
        serializer = TeamMemberSerializer(members.distinct(), many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def archived(self, request):
        """Get archived/past team members"""
        now_year = timezone.now().year
        members = self.get_queryset().filter(end_year__lt=now_year)
        serializer = TeamMemberSerializer(members, many=True, context={'request': request})
        return Response(serializer.data)