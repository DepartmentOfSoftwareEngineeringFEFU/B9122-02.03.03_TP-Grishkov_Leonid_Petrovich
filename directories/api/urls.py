from rest_framework.routers import DefaultRouter
from .views import PositionViewSet

router = DefaultRouter()
router.register(r'positions', PositionViewSet)

urlpatterns = router.urls