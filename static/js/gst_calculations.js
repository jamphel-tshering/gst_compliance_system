/**
 * Real-time GST calculations for Returns module
 * Auto-calculates GST values based on 5% rate
 */
document.addEventListener('DOMContentLoaded', function() {
    // Get the form fields
    const gstin = document.getElementById('id_gstin');
    const taxpayerName = document.getElementById('id_taxpayer_name');
    const dzongkhag = document.getElementById('id_dzongkhag');
    const organisationType = document.getElementById('id_organisation_type');
    const frequency = document.getElementById('id_frequency');
    
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
    
    // Initialize Flatpickr date picker for date fields (if not already initialized)
    let dueDatePicker = null;
    let filingDatePicker = null;
    
    if (returnDueDate && !returnDueDate._flatpickr) {
        dueDatePicker = flatpickr(returnDueDate, {
            dateFormat: 'd-m-Y',
            allowInput: true,
            parseDate: function(datestr, format) {
                // Parse DD-MM-YYYY format
                const parts = datestr.split('-');
                if (parts.length === 3) {
                    const day = parseInt(parts[0], 10);
                    const month = parseInt(parts[1], 10) - 1;
                    const year = parseInt(parts[2], 10);
                    if (!isNaN(day) && !isNaN(month) && !isNaN(year)) {
                        return new Date(year, month, day);
                    }
                }
                return null;
            },
            onChange: function(selectedDates, dateStr, instance) {
                calculateFilingDelay();
            }
        });
    }
    
    if (returnFilingDate && !returnFilingDate._flatpickr) {
        filingDatePicker = flatpickr(returnFilingDate, {
            dateFormat: 'd-m-Y',
            allowInput: true,
            parseDate: function(datestr, format) {
                // Parse DD-MM-YYYY format
                const parts = datestr.split('-');
                if (parts.length === 3) {
                    const day = parseInt(parts[0], 10);
                    const month = parseInt(parts[1], 10) - 1;
                    const year = parseInt(parts[2], 10);
                    if (!isNaN(day) && !isNaN(month) && !isNaN(year)) {
                        return new Date(year, month, day);
                    }
                }
                return null;
            },
            onChange: function(selectedDates, dateStr, instance) {
                calculateFilingDelay();
            }
        });
    }
    
    // Function to auto-fetch taxpayer information
    function fetchTaxpayerInfo() {
        if (!gstin?.value || gstin.value.length < 3) return;
        
        console.log('Fetching taxpayer info for GSTIN:', gstin.value);
        
        // Fetch taxpayer info from API
        fetch(`/api/taxpayers/taxpayers/get_by_gstin/?gstin=${gstin.value}`)
            .then(response => {
                console.log('Response status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('Taxpayer data received:', data);
                if (data && !data.error) {
                    console.log('Filling taxpayer name:', data.taxpayer_name);
                    if (taxpayerName) {
                        taxpayerName.value = data.taxpayer_name || '';
                        console.log('Taxpayer name set to:', taxpayerName.value);
                    }
                    if (dzongkhag) dzongkhag.value = data.dzongkhag || '';
                    if (organisationType) organisationType.value = data.organisation_type || '';
                    if (frequency) frequency.value = data.frequency || '';
                    console.log('Taxpayer info updated successfully');
                } else {
                    console.log('No taxpayer found or error:', data);
                }
            })
            .catch(error => {
                console.log('Error fetching taxpayer info:', error);
            });
    }
    
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
    
    // Function to calculate return due date based on tax period for Bhutan GST
    function calculateDueDate() {
        if (!taxPeriod?.value) return;
        
        const monthMap = {
            'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'Jun': 5,
            'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
        };
        
        const monthDays = {
            0: 31,  // January
            1: 28,  // February (will be adjusted for leap years)
            2: 31,  // March
            3: 30,  // April
            4: 31,  // May
            5: 30,  // June
            6: 31,  // July
            7: 31,  // August
            8: 30,  // September
            9: 31,  // October
            10: 30, // November
            11: 31  // December
        };
        
        const parts = taxPeriod.value.split('-');
        if (parts.length !== 2) return;
        
        const monthAbbr = parts[0];
        const year = parseInt(parts[1]);
        const month = monthMap[monthAbbr];
        
        if (month === undefined) return;
        
        // Adjust February for leap years
        if (month === 1) {
            const isLeapYear = (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
            monthDays[1] = isLeapYear ? 29 : 28;
        }
        
        // Get the last day of the tax period
        const lastDayOfPeriod = monthDays[month];
        const endOfPeriod = new Date(year, month, lastDayOfPeriod);
        
        // Due date is 30 days after the end of the tax period
        const dueDate = new Date(endOfPeriod);
        dueDate.setDate(dueDate.getDate() + 30);
        
        // Format as DD-MM-YYYY for display
        const day = String(dueDate.getDate()).padStart(2, '0');
        const monthNum = String(dueDate.getMonth() + 1).padStart(2, '0');
        const yearNum = dueDate.getFullYear();
        const formattedDate = `${day}-${monthNum}-${yearNum}`;
        
        if (returnDueDate) {
            returnDueDate.value = formattedDate;
            // Update Flatpickr instance if it exists
            if (dueDatePicker) {
                dueDatePicker.setDate(dueDate);
            }
        }
        console.log('Calculated due date:', formattedDate);
    }
    
    // Function to calculate filing delay
    function calculateFilingDelay() {
        if (!returnFilingDate?.value || !returnDueDate?.value) return;
        
        // Parse dates in DD-MM-YYYY format
        const parseDate = (dateStr) => {
            const parts = dateStr.split('-');
            if (parts.length === 3) {
                return new Date(parts[2], parts[1] - 1, parts[0]); // YYYY, MM-1, DD
            }
            return new Date(dateStr); // Fallback for other formats
        };
        
        const filingDate = parseDate(returnFilingDate.value);
        const dueDate = parseDate(returnDueDate.value);
        
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
    
    // GSTIN change triggers taxpayer info fetch
    if (gstin) gstin.addEventListener('blur', fetchTaxpayerInfo);
    
    // Calculate initially if values exist
    calculateGST();
    calculateDueDate();
    calculateFilingDelay();
});