/**
 * Real-time GST calculations for Returns module
 * Auto-calculates GST values based on 5% rate
 */
document.addEventListener('DOMContentLoaded', function() {
    // Get the form fields
    const declaredSales = document.getElementById('id_declared_sales');
    const declaredImportValue = document.getElementById('id_declared_import_value');
    const declaredDomesticPurchase = document.getElementById('id_declared_domestic_purchase');
    const taxPeriod = document.getElementById('id_tax_period');
    const returnFilingDate = document.getElementById('id_return_filing_date');
    const returnDueDate = document.getElementById('id_return_due_date');
    const filingDelay = document.getElementById('id_filing_delay_days');
    
    const declaredImportGST = document.getElementById('id_declared_import_gst');
    const domesticPurchaseITC = document.getElementById('id_domestic_purchase_itc_claimed');
    const declaredOutputGST = document.getElementById('id_declared_output_gst');
    const totalITCClaimed = document.getElementById('id_total_itc_claimed');
    const gstPayableRefundable = document.getElementById('id_gst_payable_refundable');
    
    // Function to calculate GST values
    function calculateGST() {
        const sales = parseFloat(declaredSales?.value) || 0;
        const importValue = parseFloat(declaredImportValue?.value) || 0;
        const domesticPurchase = parseFloat(declaredDomesticPurchase?.value) || 0;
        
        // Calculate with 5% GST rate
        const importGST = importValue * 0.05;
        const domesticITC = domesticPurchase * 0.05;
        const outputGST = sales * 0.05;
        const totalITC = importGST + domesticITC;
        const payableRefundable = outputGST - totalITC;
        
        // Update the fields
        if (declaredImportGST) declaredImportGST.value = importGST.toFixed(2);
        if (domesticPurchaseITC) domesticPurchaseITC.value = domesticITC.toFixed(2);
        if (declaredOutputGST) declaredOutputGST.value = outputGST.toFixed(2);
        if (totalITCClaimed) totalITCClaimed.value = totalITC.toFixed(2);
        if (gstPayableRefundable) gstPayableRefundable.value = payableRefundable.toFixed(2);
    }
    
    // Function to calculate return due date based on tax period
    function calculateDueDate() {
        if (!taxPeriod?.value) return;
        
        const monthMap = {
            'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'Jun': 5,
            'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
        };
        
        const parts = taxPeriod.value.split('-');
        if (parts.length !== 2) return;
        
        const monthAbbr = parts[0];
        const year = parseInt(parts[1]);
        const month = monthMap[monthAbbr];
        
        if (month === undefined) return;
        
        // Due date is 20th of the following month
        let dueDate;
        if (month === 11) { // December
            dueDate = new Date(year + 1, 0, 20);
        } else {
            dueDate = new Date(year, month + 1, 20);
        }
        
        // Format as YYYY-MM-DD for date input
        const formattedDate = dueDate.toISOString().split('T')[0];
        if (returnDueDate) returnDueDate.value = formattedDate;
    }
    
    // Function to calculate filing delay
    function calculateFilingDelay() {
        if (!returnFilingDate?.value || !returnDueDate?.value) return;
        
        const filingDate = new Date(returnFilingDate.value);
        const dueDate = new Date(returnDueDate.value);
        
        const diffTime = filingDate - dueDate;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        // Only count late days
        const delay = Math.max(0, diffDays);
        if (filingDelay) filingDelay.value = delay;
    }
    
    // Add event listeners to trigger calculations
    if (declaredSales) declaredSales.addEventListener('input', calculateGST);
    if (declaredImportValue) declaredImportValue.addEventListener('input', calculateGST);
    if (declaredDomesticPurchase) declaredDomesticPurchase.addEventListener('input', calculateGST);
    
    // Also calculate on change for better performance
    if (declaredSales) declaredSales.addEventListener('change', calculateGST);
    if (declaredImportValue) declaredImportValue.addEventListener('change', calculateGST);
    if (declaredDomesticPurchase) declaredDomesticPurchase.addEventListener('change', calculateGST);
    
    // Tax period change triggers due date calculation
    if (taxPeriod) taxPeriod.addEventListener('change', calculateDueDate);
    
    // Filing date change triggers delay calculation
    if (returnFilingDate) returnFilingDate.addEventListener('change', calculateFilingDelay);
    if (returnDueDate) returnDueDate.addEventListener('change', calculateFilingDelay);
    
    // Calculate initially if values exist
    calculateGST();
    calculateDueDate();
    calculateFilingDelay();
});