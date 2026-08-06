import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster, BusinessLicense
from django.db import transaction

def migrate_to_license_structure():
    """
    Migrate duplicate TaxpayerMaster records to new structure:
    - Keep one record per GSTIN in TaxpayerMaster
    - Move duplicates to BusinessLicense
    """
    # Get all taxpayers grouped by GSTIN
    from django.db.models import Count
    
    duplicates = TaxpayerMaster.objects.values('gstin').annotate(count=Count('id')).filter(count__gt=1)
    
    print(f"Found {duplicates.count()} GSTINs with multiple records")
    
    for dup in duplicates:
        gstin = dup['gstin']
        taxpayers = TaxpayerMaster.objects.filter(gstin=gstin).order_by('id')
        
        if taxpayers.count() > 1:
            # Keep the first one as main taxpayer
            main_taxpayer = taxpayers.first()
            print(f"\nProcessing GSTIN {gstin}: {taxpayers.count()} records")
            print(f"  Main taxpayer: {main_taxpayer.id} - {main_taxpayer.business_name}")
            
            # Move the rest to BusinessLicense
            for taxpayer in taxpayers[1:]:
                print(f"  Moving to license: {taxpayer.id} - {taxpayer.business_name}")
                
                # Create BusinessLicense from the duplicate
                license_number = f"LIC-{taxpayer.id}-{taxpayer.gstin}"
                license = BusinessLicense.objects.create(
                    taxpayer=main_taxpayer,
                    license_number=license_number,
                    ramis_tpn=taxpayer.ramis_tpn,
                    business_name=taxpayer.business_name,
                    sector=taxpayer.sector,
                    sub_sector=taxpayer.sub_sector,
                    business_activity=taxpayer.business_activity,
                    license_status=taxpayer.status,
                    remarks=f"Migrated from duplicate taxpayer record {taxpayer.id}"
                )
                print(f"  Created license: {license.license_number}")
                
                # Delete the duplicate taxpayer
                taxpayer.delete()
                print(f"  Deleted duplicate taxpayer record")
    
    print("\nMigration complete!")
    print(f"Final TaxpayerMaster count: {TaxpayerMaster.objects.count()}")
    print(f"BusinessLicense count: {BusinessLicense.objects.count()}")

if __name__ == '__main__':
    migrate_to_license_structure()