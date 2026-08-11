from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import GSTReturn
from .serializers import GSTReturnSerializer


class GSTReturnViewSet(viewsets.ModelViewSet):
    """ViewSet for GST Return model"""
    queryset = GSTReturn.objects.all()
    serializer_class = GSTReturnSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gstin', 'tax_period', 'filing_status', 'frequency']
    search_fields = ['gstin', 'taxpayer_name']
    ordering_fields = ['tax_period', 'filing_date', 'gstin']
    ordering = ['-tax_period']
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue returns"""
        from django.utils import timezone
        today = timezone.now().date()
        overdue_returns = self.queryset.filter(
            filing_status='Not Filed',
            tax_period__lt=today
        )
        serializer = self.get_serializer(overdue_returns, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get returns grouped by filing status"""
        status_data = {}
        for status in ['Filed', 'Not Filed', 'Late Filer']:
            status_data[status] = self.queryset.filter(filing_status=status).count()
        return Response(status_data)