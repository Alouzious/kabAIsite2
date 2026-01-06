from rest_framework import viewsets
from rest_framework. decorators import action
from rest_framework.response import Response
from . models import About
from .serializers import AboutSerializer

class AboutViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for About page"""
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get the current about page content"""
        try:
            about = About.objects.first()
            if about:
                serializer = self.get_serializer(about, context={'request': request})
                return Response(serializer.data)
            return Response({'detail': 'About page not configured yet.'}, status=404)
        except About.DoesNotExist:
            return Response({'detail': 'About page not found.'}, status=404)