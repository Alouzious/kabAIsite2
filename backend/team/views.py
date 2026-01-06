from rest_framework import viewsets, filters
from rest_framework. decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from . models import TeamRole, TeamMember
from .serializers import TeamRoleSerializer, TeamMemberSerializer, TeamMemberListSerializer

class TeamRoleViewSet(viewsets. ReadOnlyModelViewSet):
    """API endpoint for team roles"""
    queryset = TeamRole. objects.filter(is_active=True)
    serializer_class = TeamRoleSerializer

class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for team members"""
    queryset = TeamMember.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_executive']
    search_fields = ['name', 'title', 'bio']
    ordering_fields = ['order', 'name', 'joined_date']
    ordering = ['order', 'name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TeamMemberListSerializer
        return TeamMemberSerializer
    
    @action(detail=False, methods=['get'])
    def executive(self, request):
        """Get executive team members"""
        executives = self.get_queryset().filter(is_executive=True)
        serializer = TeamMemberListSerializer(executives, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_role(self, request):
        """Get team members grouped by role"""
        roles = TeamRole.objects.filter(is_active=True)
        result = []
        
        for role in roles:
            members = self.get_queryset().filter(role=role)
            if members.exists():
                result. append({
                    'role':  TeamRoleSerializer(role).data,
                    'members': TeamMemberListSerializer(members, many=True, context={'request': request}).data
                })
        
        return Response(result)