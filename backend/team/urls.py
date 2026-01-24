from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'members', views.TeamMemberViewSet, basename='team-member')

urlpatterns = router.urls