import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from django.db import connection

print("Comprehensive fix for decimal corruption...")

try:
    with connection.cursor() as cursor:
        # First, let's check the schema
        cursor.execute("PRAGMA table_info(compliance_complianceriskreferral)")
        columns = cursor.fetchall()
        print("Current schema:")
        for col in columns:
            print(f"  {col[1]}: {col[2]}")
        
        # Drop the new table if it exists from previous attempts
        cursor.execute("DROP TABLE IF EXISTS compliance_complianceriskreferral_new")
        
        # Create a new table with the same structure but clean data
        cursor.execute("""
            CREATE TABLE compliance_complianceriskreferral_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                risk_id VARCHAR(20) NOT NULL UNIQUE,
                gstin VARCHAR(15) NOT NULL,
                taxpayer_name VARCHAR(200),
                assessment_from_period VARCHAR(20),
                assessment_to_period VARCHAR(20),
                assessment_date DATE,
                assessment_status VARCHAR(30),
                risk_type VARCHAR(50),
                risk_indicator VARCHAR(100),
                risk_pattern VARCHAR(100),
                inherent_risk DECIMAL DEFAULT 0.0,
                control_risk DECIMAL DEFAULT 0.0,
                detection_risk DECIMAL DEFAULT 0.0,
                gst_behaviour_risk DECIMAL DEFAULT 0.0,
                transaction_risk DECIMAL DEFAULT 0.0,
                risk_score DECIMAL DEFAULT 0.0,
                risk_level VARCHAR(20),
                audit_assertion VARCHAR(50),
                risk_reason TEXT,
                system_decision VARCHAR(20),
                selection VARCHAR(20),
                referred_to VARCHAR(50),
                prescribed_officer_action TEXT,
                officer_assessment TEXT,
                additional_risk_factor TEXT,
                officer_risk_rating VARCHAR(20),
                officer_remarks TEXT,
                final_selection VARCHAR(20),
                final_referred_to VARCHAR(50),
                action_status VARCHAR(20),
                override_reason TEXT,
                override_date DATETIME,
                original_risk_score DECIMAL DEFAULT 0.0,
                original_risk_level VARCHAR(20),
                original_selection VARCHAR(20),
                original_system_decision VARCHAR(20),
                remarks TEXT,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                overridden_by_id BIGINT
            )
        """)
        
        # Copy data from old table to new table, converting all decimal fields to valid values
        cursor.execute("""
            INSERT INTO compliance_complianceriskreferral_new 
            (id, risk_id, gstin, taxpayer_name, assessment_from_period, assessment_to_period, 
             assessment_date, assessment_status, risk_type, risk_indicator, risk_pattern,
             inherent_risk, control_risk, detection_risk, gst_behaviour_risk, transaction_risk,
             risk_score, risk_level, audit_assertion, risk_reason, system_decision, selection,
             referred_to, prescribed_officer_action, officer_assessment, additional_risk_factor,
             officer_risk_rating, officer_remarks, final_selection, final_referred_to, action_status,
             override_reason, override_date, original_risk_score, original_risk_level, original_selection,
             original_system_decision, remarks, created_at, updated_at, overridden_by_id)
            SELECT id, risk_id, gstin, taxpayer_name, assessment_from_period, assessment_to_period,
                   assessment_date, assessment_status, risk_type, risk_indicator, risk_pattern,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, risk_level, audit_assertion, risk_reason,
                   system_decision, selection, referred_to, prescribed_officer_action, officer_assessment,
                   additional_risk_factor, officer_risk_rating, officer_remarks, final_selection,
                   final_referred_to, action_status, override_reason, override_date, 0.0,
                   original_risk_level, original_selection, original_system_decision, remarks,
                   created_at, updated_at, overridden_by_id
            FROM compliance_complianceriskreferral
        """)
        
        copied_count = cursor.rowcount
        print(f"Copied {copied_count} records to new table")
        
        # Drop old table
        cursor.execute("DROP TABLE compliance_complianceriskreferral")
        
        # Rename new table to old table name
        cursor.execute("ALTER TABLE compliance_complianceriskreferral_new RENAME TO compliance_complianceriskreferral")
        
        # Recreate indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS compliance_complianceriskreferral_gstin_idx ON compliance_complianceriskreferral(gstin)")
        cursor.execute("CREATE INDEX IF NOT EXISTS compliance_complianceriskreferral_tax_period_idx ON compliance_complianceriskreferral(assessment_from_period, assessment_to_period)")
        cursor.execute("CREATE INDEX IF NOT EXISTS compliance_complianceriskreferral_risk_level_idx ON compliance_complianceriskreferral(risk_level)")
        cursor.execute("CREATE INDEX IF NOT EXISTS compliance_complianceriskreferral_system_decision_idx ON compliance_complianceriskreferral(system_decision)")
        cursor.execute("CREATE INDEX IF NOT EXISTS compliance_complianceriskreferral_selection_idx ON compliance_complianceriskreferral(selection)")
        
        print("Successfully recreated table with clean data!")
        
        # Verify the fix
        cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral")
        final_count = cursor.fetchone()[0]
        print(f"Final record count: {final_count}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
