from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'settings', views.IndabaxSettingsViewSet, basename='indabax-settings')
router.register(r'events', views.IndabaxEventViewSet, basename='indabax-event')
router.register(r'speakers', views.IndabaxSpeakerViewSet, basename='indabax-speaker')
router.register(r'sessions', views.IndabaxSessionViewSet, basename='indabax-session')
router.register(r'gallery', views.IndabaxGalleryViewSet, basename='indabax-gallery')

urlpatterns = router.urls
