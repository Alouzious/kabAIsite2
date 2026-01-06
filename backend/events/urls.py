from django. urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'categories', views. EventCategoryViewSet, basename='event-category')
router.register(r'', views.EventViewSet, basename='event')

urlpatterns = router.urls
