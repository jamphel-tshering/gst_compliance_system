/**
 * Real-time automations for Enforcement & Recovery module
 * Auto-fetches taxpayer info when GSTIN entered
 */
document.addEventListener('DOMContentLoaded', function() {
    // Get the form fields
    const gstin = document.getElementById('id_gstin');
    const taxpayerName = document.getElementById('id_taxpayer_name');
    const noticeDate = document.getElementById('id_notice_date');
    
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
    
    // GSTIN change triggers taxpayer info fetch
    if (gstin) gstin.addEventListener('blur', fetchTaxpayerInfo);
    
    // Initialize Flatpickr for notice date
    if (noticeDate && !noticeDate._flatpickr) {
        flatpickr(noticeDate, {
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
});