from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core. views import api_root

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Root
    path('api/', api_root, name='api-root'),
    
    # API Endpoints
    path('api/core/', include('core.urls')),
    path('api/about/', include('about.urls')),
    path('api/news/', include('news.urls')),
    path('api/events/', include('events.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/team/', include('team.urls')),
    path('api/gallery/', include('gallery.urls')),
    path('api/partners/', include('partners.urls')),
    path('api/indabax/', include('indabax.urls')),
]

# Serve media and static files in development
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)