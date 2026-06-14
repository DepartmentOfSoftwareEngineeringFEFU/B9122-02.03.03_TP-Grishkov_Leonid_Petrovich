from rest_framework.routers import DefaultRouter
from .views import (
    PositionViewSet, WorkScheduleViewSet, CompetenceViewSet,
    WorkCategoryViewSet, OperationTypeViewSet, ExpenseCategoryViewSet,
    ProductViewSet
)

router = DefaultRouter()
router.register(r'positions', PositionViewSet)
router.register(r'work-schedules', WorkScheduleViewSet)
router.register(r'competences', CompetenceViewSet)
router.register(r'work-categories', WorkCategoryViewSet)
router.register(r'operation-types', OperationTypeViewSet)
router.register(r'expense-categories', ExpenseCategoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = router.urls