/**
 * Real-time automations for Audit Finding module
 * Auto-fetches taxpayer info when GSTIN entered (linked via audit case)
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Flatpickr for date fields if any
    const dateFields = ['id_case_closed_date'];
    dateFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field && !field._flatpickr) {
            flatpickr(field, {
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
});