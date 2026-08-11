import { Box, Typography, Card, CardContent, TextField, Button, Grid, MenuItem } from '@mui/material'

const AuditAllotment = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Audit Allotment
      </Typography>
      <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
        Manage audit assignments and allotments to assessors.
      </Typography>
      
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Search Audit Allotment..."
                size="small"
              />
            </Grid>
            <Grid item xs={6} md={1}>
              <Button variant="outlined" size="small">Template</Button>
            </Grid>
            <Grid item xs={6} md={1}>
              <Button variant="outlined" size="small">Import</Button>
            </Grid>
            <Grid item xs={6} md={1}>
              <Button variant="outlined" size="small">Export</Button>
            </Grid>
            <Grid item xs={6} md={1}>
              <Button variant="contained" size="small">Add</Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Typography variant="body2" color="textSecondary">
            Audit Allotment content will be implemented here with allotment data table and assessor management.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  )
}

export default AuditAllotment