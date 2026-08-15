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
    
    @action(detail=False, methods=['get'], authentication_classes=[], permission_classes=[])
    def get_by_gstin(self, request):
        """Get taxpayer information by GSTIN - allows unauthenticated access for admin panel"""
        gstin = request.query_params.get('gstin')
        
        try:
            # Filter by GSTIN and primary license
            taxpayer = TaxpayerMaster.objects.filter(
                gstin=gstin,
                is_primary_license=True
            ).first()
            
            if taxpayer:
                serializer = self.get_serializer(taxpayer)
                return Response(serializer.data)
            else:
                return Response({'error': 'Taxpayer not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    @action(detail=False, methods=['get'])
    def by_dzongkhag(self, request):
        """Get taxpayers grouped by dzongkhag"""
        dzongkhag_data = {}
        for dzongkhag in ['Mongar', 'Trashigang', 'Trashiyangtse', 'Lhuentse']:
            dzongkhag_data[dzongkhag] = self.queryset.filter(dzongkhag=dzongkhag).count()
        return Response(dzongkhag_data)
    
    @action(detail=False, methods=['get'])
    def fetch_info(self, request):
        """Fetch taxpayer information by GSTIN for auto-fill"""
        gstin = request.query_params.get('gstin', '').strip()
        try:
            taxpayer = TaxpayerMaster.objects.filter(gstin=gstin, is_primary_license=True).first()
            if taxpayer:
                return Response({
                    'success': True,
                    'taxpayer_name': taxpayer.taxpayer_name,
                    'cid_company_reg_no': taxpayer.cid_company_reg_no
                })
            else:
                return Response({'success': False, 'message': 'Taxpayer not found'})
        except Exception as e:
            return Response({'success': False, 'message': str(e)})


class MultipleLicenseReferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for Multiple License Reference model"""
    queryset = MultipleLicenseReference.objects.all()
    serializer_class = MultipleLicenseReferenceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['primary_gstin', 'secondary_gstin']
    search_fields = ['primary_gstin', 'secondary_gstin', 'secondary_business_name']