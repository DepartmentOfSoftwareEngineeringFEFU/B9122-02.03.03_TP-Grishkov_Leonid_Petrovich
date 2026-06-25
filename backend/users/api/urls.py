from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, UserViewSet, MeView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('me/', MeView.as_view()),
]

urlpatterns += router.urls