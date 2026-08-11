from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GSTReturnViewSet

router = DefaultRouter()
router.register(r'returns', GSTReturnViewSet, basename='return')

urlpatterns = [
    path('', include(router.urls)),
]