import { Box, Typography, Card, CardContent, Grid, Button, MenuItem, TextField } from '@mui/material'

const Reports = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Reports
      </Typography>
      <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
        Generate and export official GST reports to Excel for documentation.
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Registration
              </Typography>
              <TextField
                fullWidth
                select
                size="small"
                defaultValue=""
                sx={{ mb: 2 }}
              >
                <MenuItem value="">Select Report</MenuItem>
                <MenuItem value="taxpayer-registration">Taxpayer Registration Report</MenuItem>
              </TextField>
              <Button variant="contained" fullWidth>Export Registration Report</Button>
              <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                Exports open directly in Microsoft Excel (.xlsx)
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Returns
              </Typography>
              <TextField
                fullWidth
                select
                size="small"
                defaultValue=""
                sx={{ mb: 2 }}
              >
                <MenuItem value="">Select Report</MenuItem>
                <MenuItem value="returns-summary">Returns Summary Report</MenuItem>
                <MenuItem value="filing-status">Filing Status Report</MenuItem>
              </TextField>
              <Button variant="contained" fullWidth>Export Returns Report</Button>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Compliance
              </Typography>
              <TextField
                fullWidth
                select
                size="small"
                defaultValue=""
                sx={{ mb: 2 }}
              >
                <MenuItem value="">Select Report</MenuItem>
                <MenuItem value="compliance-monitoring">Compliance Monitoring Report</MenuItem>
                <MenuItem value="risk-assessment">Risk Assessment Report</MenuItem>
              </TextField>
              <Button variant="contained" fullWidth>Export Compliance Report</Button>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Audit
              </Typography>
              <TextField
                fullWidth
                select
                size="small"
                defaultValue=""
                sx={{ mb: 2 }}
              >
                <MenuItem value="">Select Report</MenuItem>
                <MenuItem value="audit-summary">Audit Summary Report</MenuItem>
                <MenuItem value="audit-discrepancy">Audit Discrepancy Report</MenuItem>
              </TextField>
              <Button variant="contained" fullWidth>Export Audit Report</Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

export default Reports