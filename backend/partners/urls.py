from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'categories', views.PartnerCategoryViewSet, basename='partner-category')
router.register(r'', views.PartnerViewSet, basename='partner')

urlpatterns = router.urls
