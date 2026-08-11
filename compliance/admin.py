from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from django import forms
from django.forms import DateInput
from django.db.models import Count, Q
from django.utils.html import format_html
from .models import ComplianceMonitoring
from returns.models import GSTReturn
from taxpayers.models import TaxpayerMaster



class CustomDateInput(DateInput):
    """Custom date input with calendar picker"""
    input_type = 'date'
    
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs.update({
            'class': 'vDateField',
            'type': 'date',
        })
        super().__init__(attrs=attrs)


class ComplianceMonitoringForm(forms.ModelForm):
    """Custom form with date pickers"""
    class Meta:
        model = ComplianceMonitoring
        fields = '__all__'
        widgets = {
            'assessment_from': CustomDateInput(),
            'assessment_to': CustomDateInput(),
        }


@admin.register(ComplianceMonitoring)
class ComplianceMonitoringAdmin(admin.ModelAdmin):
    form = ComplianceMonitoringForm
    list_display = ['taxpayer', 'assessment_from', 'assessment_to', 'compliance_status', 'trust_level', 'compliance_score', 'assessment_date']
    list_display_links = ['taxpayer']
    list_filter = ['compliance_status', 'trust_level', 'filing_on_time', 'payment_on_time', 'notification_compliance', 'assessment_from', 'assessment_to']
    search_fields = ['taxpayer__taxpayer_name', 'taxpayer__gstin']
    ordering = ['-assessment_date', 'taxpayer']
    list_per_page = 50  # Show more records in tabular view
    
    fieldsets = (
        ('Simple Assessment', {
            'fields': ('taxpayer', 'assessment_from', 'assessment_to')
        }),
        ('Auto-Generated Metrics (Read Only)', {
            'fields': ('filing_on_time', 'payment_on_time', 'notification_compliance', 'trust_level', 'trust_score', 'compliance_status', 'compliance_score'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('compliance_notes',)
        }),
    )
    
    readonly_fields = ['filing_on_time', 'payment_on_time', 'notification_compliance', 'trust_level', 'trust_score', 'compliance_status', 'compliance_score', 'assessment_date', 'created_at', 'updated_at']
    
    def get_readonly_fields(self, request, obj=None):
        """Hide auto-generated metrics when adding new record"""
        if obj is None:  # Adding new record
            return ['assessment_date', 'created_at', 'updated_at']
        return self.readonly_fields
    
    def get_fieldsets(self, request, obj=None):
        """Hide auto-generated metrics when adding new record"""
        if obj is None:  # Adding new record
            return (
                ('Simple Assessment', {
                    'fields': ('taxpayer', 'assessment_from', 'assessment_to')
                }),
                ('Notes', {
                    'fields': ('compliance_notes',)
                }),
            )
        return self.fieldsets
    
    actions = ['auto_generate_compliance', 'mark_as_compliant', 'mark_as_non_compliant', 'auto_populate_all_taxpayers']
    
    def changelist_view(self, request, extra_context=None):
        """Override to show compliance dashboard"""
        response = super().changelist_view(request, extra_context)
        
        # Calculate compliance statistics
        total_taxpayers = TaxpayerMaster.objects.filter(is_primary_license=True).count()
        compliant_count = self.get_queryset(request).filter(compliance_status__in=['excellent', 'good']).count()
        non_compliant_count = self.get_queryset(request).filter(compliance_status__in=['poor', 'critical']).count()
        fair_count = self.get_queryset(request).filter(compliance_status='fair').count()
        
        # Add to context
        extra_context = extra_context or {}
        extra_context.update({
            'total_taxpayers': total_taxpayers,
            'compliant_count': compliant_count,
            'non_compliant_count': non_compliant_count,
            'fair_count': fair_count,
            'needs_assessment': total_taxpayers - self.get_queryset(request).count(),
        })
        
        return response
    
    def auto_populate_all_taxpayers(self, request, queryset):
        """Auto-populate compliance for all taxpayers from GST returns"""
        count = 0
        taxpayers = TaxpayerMaster.objects.filter(is_primary_license=True)
        
        for taxpayer in taxpayers:
            # Get latest GST return for this taxpayer
            latest_return = GSTReturn.objects.filter(
                gstin=taxpayer.gstin
            ).order_by('-tax_period').first()
            
            if latest_return:
                # Check if compliance record already exists for this period
                existing = ComplianceMonitoring.objects.filter(
                    taxpayer=taxpayer,
                    gst_return=latest_return
                ).first()
                
                if not existing:
                    # Create new compliance record
                    compliance = ComplianceMonitoring.objects.create(
                        taxpayer=taxpayer,
                        gst_return=latest_return,
                        assessment_from=latest_return.return_due_date,
                        assessment_to=timezone.now().date(),
                        filing_on_time=latest_return.filing_delay_days == 0,
                        payment_on_time=latest_return.payment_status == 'paid',
                        notification_compliance=latest_return.compliance_status == 'compliant',
                        assessed_by=request.user
                    )
                    
                    # Auto-calculate trust level only if we have actual return data
                    if compliance.filing_on_time and compliance.payment_on_time:
                        compliance.trust_level = 'trustworthy'
                        compliance.trust_score = 75
                    elif compliance.filing_on_time or compliance.payment_on_time:
                        compliance.trust_level = 'moderate'
                        compliance.trust_score = 50
                    else:
                        compliance.trust_level = 'low_trust'
                        compliance.trust_score = 25
                    
                    compliance.save()
                    count += 1
        
        if count > 0:
            self.message_user(request, f'Auto-populated compliance for {count} taxpayers from GST returns.')
        else:
            self.message_user(request, 'No new compliance records created. Either no GST returns found or records already exist.', messages.WARNING)
    
    auto_populate_all_taxpayers.short_description = 'Auto-populate compliance for all taxpayers'
    
    def mark_as_compliant(self, request, queryset):
        """Mark selected records as compliant"""
        count = queryset.update(
            filing_on_time=True,
            payment_on_time=True,
            notification_compliance=True,
            trust_level='trustworthy',
            trust_score=75
        )
        # Recalculate scores
        for obj in queryset:
            obj.save()
        self.message_user(request, f'Marked {count} records as compliant.')
    
    mark_as_compliant.short_description = 'Mark as Compliant'
    
    def mark_as_non_compliant(self, request, queryset):
        """Mark selected records as non-compliant"""
        count = queryset.update(
            filing_on_time=False,
            payment_on_time=False,
            notification_compliance=False,
            trust_level='low_trust',
            trust_score=25
        )
        # Recalculate scores
        for obj in queryset:
            obj.save()
        self.message_user(request, f'Marked {count} records as non-compliant.')
    
    mark_as_non_compliant.short_description = 'Mark as Non-Compliant'
    
    def auto_generate_compliance(self, request, queryset):
        """Auto-generate compliance data from GST returns"""
        count = 0
        for compliance in queryset:
            if compliance.taxpayer:
                # Get latest GST return for this taxpayer
                latest_return = GSTReturn.objects.filter(
                    gstin=compliance.taxpayer.gstin
                ).order_by('-tax_period').first()
                
                if latest_return:
                    # Auto-calculate metrics from GST return
                    compliance.filing_on_time = latest_return.filing_delay_days == 0
                    compliance.payment_on_time = latest_return.payment_status == 'paid'
                    compliance.notification_compliance = latest_return.compliance_status == 'compliant'
                    
                    # Auto-calculate trust level based on compliance
                    if compliance.filing_on_time and compliance.payment_on_time:
                        compliance.trust_level = 'trustworthy'
                        compliance.trust_score = 75
                    elif compliance.filing_on_time or compliance.payment_on_time:
                        compliance.trust_level = 'moderate'
                        compliance.trust_score = 50
                    else:
                        compliance.trust_level = 'low_trust'
                        compliance.trust_score = 25
                    
                    compliance.gst_return = latest_return
                    compliance.save()
                    count += 1
        
        self.message_user(request, f'Auto-generated compliance for {count} taxpayers from GST returns.')
    
    auto_generate_compliance.short_description = 'Auto-generate compliance from GST returns'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new record
            obj.assessed_by = request.user
            obj.assessment_date = timezone.now().date()
            
            # Auto-generate from GST return if taxpayer selected
            if obj.taxpayer:
                latest_return = GSTReturn.objects.filter(
                    gstin=obj.taxpayer.gstin
                ).order_by('-tax_period').first()
                
                if latest_return:
                    obj.filing_on_time = latest_return.filing_delay_days == 0
                    obj.payment_on_time = latest_return.payment_status == 'paid'
                    obj.notification_compliance = latest_return.compliance_status == 'compliant'
                    obj.gst_return = latest_return
                    
                    # Auto-calculate trust level
                    if obj.filing_on_time and obj.payment_on_time:
                        obj.trust_level = 'trustworthy'
                        obj.trust_score = 75
                    elif obj.filing_on_time or obj.payment_on_time:
                        obj.trust_level = 'moderate'
                        obj.trust_score = 50
                    else:
                        obj.trust_level = 'low_trust'
                        obj.trust_score = 25
            
        super().save_model(request, obj, form, change)
