from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'roles', views.TeamRoleViewSet, basename='team-role')
router.register(r'members', views.TeamMemberViewSet, basename='team-member')

urlpatterns = router.urls
