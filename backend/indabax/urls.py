from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'settings', views.IndabaxSettingsViewSet, basename='indabax-settings')
router.register(r'events', views.IndabaxEventViewSet, basename='indabax-event')
router.register(r'speakers', views.IndabaxSpeakerViewSet, basename='indabax-speaker')
router.register(r'sessions', views.IndabaxSessionViewSet, basename='indabax-session')
router.register(r'gallery', views.IndabaxGalleryViewSet, basename='indabax-gallery')
router.register(r'leaders', views.LeaderViewSet, basename='indabax-leader')

urlpatterns = [
    path('resources/', views.LearningResourceListView.as_view(), name='indabax-resources-api'),
    path('hero/', views.HeroSectionListView.as_view(), name='indabax-hero-api'),
    path('', include(router.urls)),
]