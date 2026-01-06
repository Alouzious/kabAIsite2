from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'categories', views.ProjectCategoryViewSet, basename='project-category')
router.register(r'', views.ProjectViewSet, basename='project')

urlpatterns = router.urls
