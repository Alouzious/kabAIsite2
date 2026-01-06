from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'categories', views.GalleryCategoryViewSet, basename='gallery-category')
router.register(r'images', views.GalleryImageViewSet, basename='gallery-image')

urlpatterns = router.urls
