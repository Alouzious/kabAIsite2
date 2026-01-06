from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'categories', views.NewsCategoryViewSet, basename='news-category')
router.register(r'articles', views.NewsViewSet, basename='news')

urlpatterns = router.urls
