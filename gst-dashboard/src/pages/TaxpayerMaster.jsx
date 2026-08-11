import { Box, Typography, Card, CardContent, TextField, Button, Grid, MenuItem, List, ListItem, ListItemButton, ListItemText, Divider, AppBar, Toolbar } from '@mui/material'
import { Logout as LogoutIcon } from '@mui/icons-material'

const TaxpayerMaster = ({ onNavigate, onLogout }) => {
  return (
    <Box sx={{ display: 'flex' }}>
      {/* Sidebar */}
      <Box sx={{ width: 280, bgcolor: '#f5f5f5', minHeight: '100vh', borderRight: '1px solid #ddd' }}>
        <Box sx={{ p: 2, bgcolor: '#1976d2', color: 'white' }}>
          <Typography variant="h6">GST Management System</Typography>
        </Box>
        <List>
          <ListItemButton onClick={() => onNavigate('dashboard')}>
            <ListItemText primary="Dashboard" />
          </ListItemButton>
          <ListItemButton selected>
            <ListItemText primary="Taxpayer Master" />
          </ListItemButton>
          <ListItemButton onClick={() => onNavigate('returns')}>
            <ListItemText primary="GST Returns" />
          </ListItemButton>
          <ListItemButton onClick={() => onNavigate('compliance')}>
            <ListItemText primary="Compliance Risk" />
          </ListItemButton>
          <ListItemButton onClick={() => onNavigate('audit-allotment')}>
            <ListItemText primary="Audit Allotment" />
          </ListItemButton>
          <ListItemButton onClick={() => onNavigate('audit-register')}>
            <ListItemText primary="Audit Register" />
          </ListItemButton>
          <ListItemButton onClick={() => onNavigate('reports')}>
            <ListItemText primary="Reports" />
          </ListItemButton>
          <ListItemButton onClick={() => onNavigate('user-management')}>
            <ListItemText primary="User Management" />
          </ListItemButton>
          <ListItemButton onClick={() => onNavigate('system-settings')}>
            <ListItemText primary="System Settings" />
          </ListItemButton>
          <Divider />
          <ListItemButton onClick={onLogout}>
            <ListItemIcon><LogoutIcon /></ListItemIcon>
            <ListItemText primary="Sign out" />
          </ListItemButton>
        </List>
      </Box>

      {/* Main Content */}
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static" sx={{ mb: 3 }}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Goods and Services Tax (GST) - RRCO, Mongar
            </Typography>
            <Typography variant="body2" sx={{ display: { xs: 'none', md: 'block' } }}>
              Ministry of Finance | Royal Government of Bhutan
            </Typography>
          </Toolbar>
        </AppBar>

        <Box sx={{ p: 3 }}>
          <Typography variant="h4" gutterBottom>
            Taxpayer Master (Primary)
          </Typography>
          <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
            Primary GST-registered taxpayers allotted a GSTIN. Add directly or import from Excel.
          </Typography>
          
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs={12} md={3}>
                  <TextField
                    fullWidth
                    label="Search Taxpayer Master (Primary)..."
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

          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12} md={2}>
                  <TextField
                    fullWidth
                    label="Month From"
                    select
                    size="small"
                    defaultValue=""
                  >
                    <MenuItem value="">---------</MenuItem>
                  </TextField>
                </Grid>
                <Grid item xs={12} md={2}>
                  <TextField
                    fullWidth
                    label="Month To"
                    select
                    size="small"
                    defaultValue=""
                  >
                    <MenuItem value="">---------</MenuItem>
                  </TextField>
                </Grid>
                <Grid item xs={12} md={2}>
                  <TextField
                    fullWidth
                    label="GSTIN"
                    size="small"
                    placeholder="Search GSTIN..."
                  />
                </Grid>
                <Grid item xs={12} md={2}>
                  <TextField
                    fullWidth
                    label="Dzongkhag"
                    select
                    size="small"
                    defaultValue="All"
                  >
                    <MenuItem value="All">All</MenuItem>
                    <MenuItem value="Mongar">Mongar</MenuItem>
                    <MenuItem value="Trashigang">Trashigang</MenuItem>
                    <MenuItem value="Trashiyangtse">Trashiyangtse</MenuItem>
                    <MenuItem value="Lhuentse">Lhuentse</MenuItem>
                  </TextField>
                </Grid>
                <Grid item xs={12} md={2}>
                  <TextField
                    fullWidth
                    label="Frequency"
                    select
                    size="small"
                    defaultValue="All"
                  >
                    <MenuItem value="All">All</MenuItem>
                    <MenuItem value="Monthly">Monthly</MenuItem>
                    <MenuItem value="Quarterly">Quarterly</MenuItem>
                    <MenuItem value="Half Yearly">Half Yearly</MenuItem>
                  </TextField>
                </Grid>
                <Grid item xs={12} md={2}>
                  <TextField
                    fullWidth
                    label="Organisation Type"
                    select
                    size="small"
                    defaultValue="All"
                  >
                    <MenuItem value="All">All</MenuItem>
                    <MenuItem value="Sole Proprietorship">Sole Proprietorship</MenuItem>
                    <MenuItem value="Private Company">Private Company</MenuItem>
                    <MenuItem value="Public Company">Public Company</MenuItem>
                    <MenuItem value="Partnership">Partnership</MenuItem>
                  </TextField>
                </Grid>
              </Grid>
            </CardContent>
          </Card>

          <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
            Taxpayer Master (Primary) content will be implemented here with data table.
          </Typography>
        </Box>
      </Box>
    </Box>
  )
}

export default TaxpayerMaster