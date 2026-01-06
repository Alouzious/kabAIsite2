from django. urls import path, include
from rest_framework.routers import SimpleRouter
from .  import views

router = SimpleRouter()
router.register(r'site-settings', views.SiteSettingsViewSet, basename='site-settings')
router.register(r'hero-slides', views.HeroSlideViewSet, basename='hero-slides')
router.register(r'contact-info', views.ContactInfoViewSet, basename='contact-info')
router.register(r'quick-links', views.QuickLinkViewSet, basename='quick-links')

urlpatterns = router.urls
