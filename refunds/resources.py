from import_export import resources
from .models import RefundRegister

class RefundRegisterResource(resources.ModelResource):
    class Meta:
        model = RefundRegister
        fields = (
            'refund_id', 'gst_tpn', 'taxpayer_name',
            'tax_period', 'claim_date', 'claimed_amount',
            'adjustment', 'refund_disallowed', 'refund_approved', 'refund_adjustment_percentage',
            'processing_days', 'processed_date', 'processed_by',
            'status', 'refund_reason', 'reason_code', 'remarks'
        )
        export_order = (
            'refund_id', 'gst_tpn', 'taxpayer_name',
            'tax_period', 'claim_date', 'claimed_amount',
            'adjustment', 'refund_disallowed', 'refund_approved', 'refund_adjustment_percentage',
            'processing_days', 'processed_date', 'processed_by',
            'status', 'refund_reason', 'reason_code', 'remarks'
        )
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['refund_id']