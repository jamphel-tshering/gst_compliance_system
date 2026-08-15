from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaxpayerMasterViewSet, MultipleLicenseReferenceViewSet

router = DefaultRouter()
router.register(r'taxpayers', TaxpayerMasterViewSet, basename='taxpayer')
router.register(r'licenses', MultipleLicenseReferenceViewSet, basename='license')

urlpatterns = [
    path('', include(router.urls)),
    path('taxpayers/get_by_gstin/', TaxpayerMasterViewSet.as_view({'get': 'get_by_gstin'}), name='taxpayer-by-gstin'),
]