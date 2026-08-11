from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import TaxpayerMaster, MultipleLicenseReference
from .serializers import TaxpayerMasterSerializer, MultipleLicenseReferenceSerializer


class TaxpayerMasterViewSet(viewsets.ModelViewSet):
    """ViewSet for Taxpayer Master model"""
    queryset = TaxpayerMaster.objects.all()
    serializer_class = TaxpayerMasterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gstin', 'dzongkhag', 'frequency', 'organisation_type', 'status', 'is_primary_license']
    search_fields = ['gstin', 'taxpayer_name', 'business_name']
    ordering_fields = ['taxpayer_name', 'registration_date', 'gstin']
    ordering = ['taxpayer_name']
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active taxpayers"""
        active_taxpayers = self.queryset.filter(status='Active')
        serializer = self.get_serializer(active_taxpayers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_dzongkhag(self, request):
        """Get taxpayers grouped by dzongkhag"""
        dzongkhag_data = {}
        for dzongkhag in ['Mongar', 'Trashigang', 'Trashiyangtse', 'Lhuentse']:
            dzongkhag_data[dzongkhag] = self.queryset.filter(dzongkhag=dzongkhag).count()
        return Response(dzongkhag_data)


class MultipleLicenseReferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for Multiple License Reference model"""
    queryset = MultipleLicenseReference.objects.all()
    serializer_class = MultipleLicenseReferenceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['primary_gstin', 'secondary_gstin']
    search_fields = ['primary_gstin', 'secondary_gstin', 'secondary_business_name']