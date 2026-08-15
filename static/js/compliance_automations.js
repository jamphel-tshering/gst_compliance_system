/**
 * Real-time automations for Compliance & Enforcement module
 * Auto-fetches taxpayer info and calculates filing delay
 */
document.addEventListener('DOMContentLoaded', function() {
    // Get the form fields
    const gstin = document.getElementById('id_gstin');
    const taxpayerName = document.getElementById('id_taxpayer_name');
    const taxPeriod = document.getElementById('id_tax_period');
    const assessmentDate = document.getElementById('id_assessment_date');
    
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
                    console.log('Taxpayer info updated successfully');
                } else {
                    console.log('No taxpayer found or error:', data);
                }
            })
            .catch(error => {
                console.log('Error fetching taxpayer info:', error);
            });
    }
    
    // Function to auto-calculate filing delay based on tax period
    function calculateFilingDelay() {
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
        
        // Calculate filing delay (assuming assessment date is current date)
        const today = new Date();
        const delay = Math.max(0, Math.ceil((today - dueDate) / (1000 * 60 * 60 * 24)));
        
        // Update filing delay field if it exists
        const filingDelayField = document.getElementById('id_filing_delay');
        if (filingDelayField) {
            filingDelayField.value = delay;
        }
        
        console.log('Calculated filing delay:', delay, 'days');
    }
    
    // GSTIN change triggers taxpayer info fetch
    if (gstin) gstin.addEventListener('blur', fetchTaxpayerInfo);
    
    // Tax period change triggers filing delay calculation
    if (taxPeriod) taxPeriod.addEventListener('change', calculateFilingDelay);
    
    // Initialize Flatpickr for assessment date
    if (assessmentDate && !assessmentDate._flatpickr) {
        flatpickr(assessmentDate, {
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
            }
        });
    }
    
    // Calculate initially if values exist
    calculateFilingDelay();
});