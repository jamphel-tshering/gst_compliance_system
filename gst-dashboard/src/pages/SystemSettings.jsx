import { Box, Typography, Card, CardContent, TextField, Button, Grid, MenuItem } from '@mui/material'

const SystemSettings = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        System Settings
      </Typography>
      <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
        Configure your regional GST office details, rates and penalties used across reports.
      </Typography>
      
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Office & Tax Configuration
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 3 }}>
            These values are referenced in official reports and computations.
          </Typography>
          
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Regional GST Office Name *"
                defaultValue="Regional Revenue and Customs office"
                size="small"
                sx={{ mb: 2 }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Office Address"
                defaultValue="NRDCL Building, Below Dzong, mongar"
                size="small"
                sx={{ mb: 2 }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Office Contact No."
                defaultValue="+975 2 322 111"
                size="small"
                sx={{ mb: 2 }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Office Email"
                defaultValue="gst-thimphu@rgob.gov.bt"
                size="small"
                sx={{ mb: 2 }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Current Financial Year"
                defaultValue="2026-27"
                helperText="e.g. 2026-27"
                size="small"
                sx={{ mb: 2 }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Standard GST Rate (%)"
                defaultValue="7"
                type="number"
                size="small"
                sx={{ mb: 2 }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Monthly Return Due Day"
                defaultValue="15"
                type="number"
                size="small"
                sx={{ mb: 2 }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Late Filing Penalty (BTN)"
                defaultValue="500"
                type="number"
                size="small"
                sx={{ mb: 2 }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Late Payment Interest (% p.m.)"
                defaultValue="1.5"
                type="number"
                size="small"
                sx={{ mb: 2 }}
              />
            </Grid>
          </Grid>
          
          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            Report Signature Block
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
            Commissioner, GST & Customs<br />
            Royal Government of Bhutan
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
            Name, designation & office shown on exported reports
          </Typography>
          
          <TextField
            fullWidth
            label="Remarks"
            defaultValue="Default configuration"
            multiline
            rows={2}
            sx={{ mb: 2 }}
          />
          
          <Button variant="contained">Save Settings</Button>
        </CardContent>
      </Card>
    </Box>
  )
}

export default SystemSettings