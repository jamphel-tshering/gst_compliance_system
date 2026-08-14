# This script will fix the assess_period method in the risk engine
# The issue is that there's a variable naming conflict between 'assessments' and 'new_assessments'

def fix_assess_period():
    with open('compliance/risk_engine.py', 'r') as f:
        content = f.read()
    
    # Find and replace the problematic lines
    old_code = """        # Apply audit targets if we have assessments
        if len(assessments) > 0:
            new_assessments = self.apply_audit_targets(assessments)
            # Save the updated assessments
            for assessment in assessments:
                assessment.save()"""
    
    new_code = """        # Apply audit targets if we have new assessments
        if len(new_assessments) > 0:
            new_assessments = self.apply_audit_targets(new_assessments)
            # Save the updated assessments
            for assessment in new_assessments:
                assessment.save()"""
    
    content = content.replace(old_code, new_code)
    
    with open('compliance/risk_engine.py', 'w') as f:
        f.write(content)
    
    print("Fixed assess_period method in risk_engine.py")

if __name__ == "__main__":
    fix_assess_period()