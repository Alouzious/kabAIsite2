from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework. response import Response
from . models import SiteSettings, HeroSlide, ContactInfo, QuickLink
from .serializers import (
    SiteSettingsSerializer, 
    HeroSlideSerializer, 
    ContactInfoSerializer,
    QuickLinkSerializer
)

class SiteSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for site settings"""
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer

class HeroSlideViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for hero slides"""
    queryset = HeroSlide.objects.filter(is_active=True)
    serializer_class = HeroSlideSerializer

class ContactInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for contact information"""
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer

class QuickLinkViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for quick links"""
    queryset = QuickLink. objects.filter(is_active=True)
    serializer_class = QuickLinkSerializer

@api_view(['GET'])
def api_root(request):
    """API root endpoint with all available endpoints"""
    base_url = request.build_absolute_uri('/api/')
    
    return Response({
        'message': 'KUAI Club API',
        'version': '1.0',
        'documentation': base_url + 'docs/',
        'endpoints':  {
            'core': {
                'site_settings': base_url + 'core/site-settings/',
                'hero_slides': base_url + 'core/hero-slides/',
                'contact_info': base_url + 'core/contact-info/',
                'quick_links': base_url + 'core/quick-links/',
            },
            'about': {
                'about':  base_url + 'about/',
                'current':  base_url + 'about/current/',
            },
            'news': {
                'categories': base_url + 'news/categories/',
                'articles': base_url + 'news/articles/',
            },
            'events': {
                'categories': base_url + 'events/categories/',
                'events': base_url + 'events/',
                'upcoming': base_url + 'events/upcoming/',
                'past': base_url + 'events/past/',
                'featured': base_url + 'events/featured/',
            },
            'projects': {
                'categories': base_url + 'projects/categories/',
                'projects':  base_url + 'projects/',
                'featured': base_url + 'projects/featured/',
                'by_status': base_url + 'projects/by_status/',
            },
            'team': {
                'roles':  base_url + 'team/roles/',
                'members': base_url + 'team/members/',
                'executive': base_url + 'team/members/executive/',
                'by_role': base_url + 'team/members/by_role/',
            },
            'gallery': {
                'categories': base_url + 'gallery/categories/',
                'images': base_url + 'gallery/images/',
                'featured': base_url + 'gallery/images/featured/',
                'by_category': base_url + 'gallery/images/by_category/',
            },
            'partners': {
                'categories': base_url + 'partners/categories/',
                'partners': base_url + 'partners/',
                'featured': base_url + 'partners/featured/',
                'by_category': base_url + 'partners/by_category/',
            },
            'indabax':  {
                'settings': base_url + 'indabax/settings/',
                'events': base_url + 'indabax/events/',
                'latest_event': base_url + 'indabax/events/latest/',
                'speakers':  base_url + 'indabax/speakers/',
                'keynote_speakers': base_url + 'indabax/speakers/keynote/',
                'sessions':  base_url + 'indabax/sessions/',
                'gallery': base_url + 'indabax/gallery/',
            },
        }
    })