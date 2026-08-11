import { useState, useEffect } from 'react'
import { Box, Typography, Tabs, Tab, Grid, Card, CardContent, TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Dialog, DialogTitle, DialogContent, DialogActions, FormControl, InputLabel, Select, MenuItem, InputAdornment, CircularProgress, Alert } from '@mui/material'
import { Search, Add, Edit, Delete, CloudUpload, CloudDownload } from '@mui/icons-material'

const API_BASE_URL = 'http://localhost:8000/taxpayers'

const Registration = () => {
  const [tab, setTab] = useState(0)
  const [searchTerm, setSearchTerm] = useState('')
  const [editDialogOpen, setEditDialogOpen] = useState(false)
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
  const [selectedTaxpayer, setSelectedTaxpayer] = useState(null)
  
  const [primaryTaxpayers, setPrimaryTaxpayers] = useState([])
  const [secondaryTaxpayers, setSecondaryTaxpayers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch data from backend
  useEffect(() => {
    fetchTaxpayers()
  }, [])

  const fetchTaxpayers = async () => {
    try {
      setLoading(true)
      setError(null)
      
      console.log('Fetching taxpayers from:', `${API_BASE_URL}/taxpayers/`)
      
      // Fetch all taxpayers
      const response = await fetch(`${API_BASE_URL}/taxpayers/`)
      console.log('Response status:', response.status)
      
      if (!response.ok) {
        const errorText = await response.text()
        console.error('Error response:', errorText)
        throw new Error(`Failed to fetch taxpayers: ${response.status} - ${errorText}`)
      }
      
      const data = await response.json()
      console.log('Fetched data:', data)
      
      const allTaxpayers = data.results || data || []
      console.log('Total taxpayers:', allTaxpayers.length)
      
      // Filter on frontend based on is_primary_license
      const primary = allTaxpayers.filter(t => t.is_primary_license === true)
      const secondary = allTaxpayers.filter(t => t.is_primary_license === false)
      
      console.log('Primary taxpayers:', primary.length)
      console.log('Secondary taxpayers:', secondary.length)
      
      setPrimaryTaxpayers(primary)
      setSecondaryTaxpayers(secondary)
    } catch (err) {
      console.error('Error fetching taxpayers:', err)
      setError(`Failed to load taxpayer data: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleTabChange = (event, newValue) => {
    setTab(newValue)
  }

  const handleEdit = (taxpayer) => {
    setSelectedTaxpayer(taxpayer)
    setEditDialogOpen(true)
  }

  const handleDelete = (taxpayer) => {
    setSelectedTaxpayer(taxpayer)
    setDeleteDialogOpen(true)
  }

  const handleAdd = () => {
    setSelectedTaxpayer(null)
    setEditDialogOpen(true)
  }

  const filteredPrimary = primaryTaxpayers.filter(t => 
    (t.gstin && t.gstin.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (t.taxpayer_name && t.taxpayer_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (t.business_name && t.business_name.toLowerCase().includes(searchTerm.toLowerCase()))
  )

  const filteredSecondary = secondaryTaxpayers.filter(t => 
    (t.gstin && t.gstin.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (t.business_name && t.business_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (t.taxpayer_name && t.taxpayer_name.toLowerCase().includes(searchTerm.toLowerCase()))
  )

  return (
    <Box sx={{ p: 4, bgcolor: '#fafafa', minHeight: '100vh' }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" gutterBottom sx={{ fontWeight: 700, color: '#1a237e', mb: 1 }}>
          Taxpayer Registration
        </Typography>
        <Typography variant="body1" color="#616161" sx={{ fontSize: '1rem' }}>
          Manage primary taxpayer registrations and secondary business licenses
        </Typography>
      </Box>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tab} onChange={handleTabChange} sx={{ '& .MuiTab-root': { fontWeight: 600 } }}>
          <Tab label="Primary Taxpayer" />
          <Tab label="Secondary Businesses" />
        </Tabs>
      </Box>

      {tab === 0 && (
        <Box>
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
              <CircularProgress />
            </Box>
          ) : error ? (
            <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>
          ) : (
            <>
              {/* Search and Actions */}
              <Card sx={{ mb: 3, boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid #e0e0e0' }}>
                <CardContent sx={{ p: 3 }}>
                  <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} md={5}>
                      <TextField
                        fullWidth
                        label="Search Taxpayers..."
                        size="small"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        InputProps={{
                          endAdornment: (
                            <InputAdornment position="end">
                              <Search />
                            </InputAdornment>
                          )
                        }}
                      />
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Button variant="outlined" size="small" startIcon={<CloudUpload />}>
                        Import
                      </Button>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Button variant="outlined" size="small" startIcon={<CloudDownload />}>
                        Export
                      </Button>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Button variant="contained" size="small" startIcon={<Add />} onClick={handleAdd}>
                        Add
                      </Button>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>

              {/* Primary Taxpayer Table */}
              <Card sx={{ boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid #e0e0e0' }}>
                <CardContent sx={{ p: 3 }}>
                  <TableContainer sx={{ maxHeight: 500 }}>
                    <Table stickyHeader size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 120 }}>GSTIN</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 200 }}>Taxpayer Name</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 200 }}>Business Name</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 130 }}>CID/Co. Reg No</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 120 }}>RAMIS TPN</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 130 }}>License Number</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 100 }}>Status</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 120 }}>Dzongkhag</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 120 }}>Sector</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 130 }}>Sub-Sector</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 150 }}>Business Activity</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 150 }}>Organisation Type</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 100 }}>Frequency</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 120 }}>Reg. Date</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 120 }}>Commencement Date</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 180 }}>Email</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 130 }}>Mobile</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 200 }}>Business Address</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 150 }}>Remarks</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 100 }}>Actions</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {filteredPrimary.length > 0 ? (
                          filteredPrimary.map((taxpayer) => (
                            <TableRow key={taxpayer.id} hover sx={{ '&:hover': { bgcolor: '#f5f5f5' } }}>
                              <TableCell>{taxpayer.gstin || '-'}</TableCell>
                              <TableCell>{taxpayer.taxpayer_name || '-'}</TableCell>
                              <TableCell>{taxpayer.business_name || '-'}</TableCell>
                              <TableCell>{taxpayer.cid_company_reg_no || '-'}</TableCell>
                              <TableCell>{taxpayer.ramis_tpn || '-'}</TableCell>
                              <TableCell>{taxpayer.license_number || '-'}</TableCell>
                              <TableCell>
                                <Typography sx={{ color: taxpayer.status === 'Active' ? '#2e7d32' : '#d32f2f', fontWeight: 'bold' }}>
                                  {taxpayer.status || '-'}
                                </Typography>
                              </TableCell>
                              <TableCell>{taxpayer.dzongkhag || '-'}</TableCell>
                              <TableCell>{taxpayer.sector || '-'}</TableCell>
                              <TableCell>{taxpayer.sub_sector || '-'}</TableCell>
                              <TableCell>{taxpayer.business_activity || '-'}</TableCell>
                              <TableCell>{taxpayer.organisation_type || '-'}</TableCell>
                              <TableCell>{taxpayer.frequency || '-'}</TableCell>
                              <TableCell>{taxpayer.registration_date || '-'}</TableCell>
                              <TableCell>{taxpayer.commencement_date || '-'}</TableCell>
                              <TableCell>{taxpayer.email_address || '-'}</TableCell>
                              <TableCell>{taxpayer.mobile_number || '-'}</TableCell>
                              <TableCell sx={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{taxpayer.business_address || '-'}</TableCell>
                              <TableCell sx={{ maxWidth: 150, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{taxpayer.remarks || '-'}</TableCell>
                              <TableCell>
                                <Button size="small" onClick={() => handleEdit(taxpayer)} startIcon={<Edit />} sx={{ mr: 1 }}>
                                  Edit
                                </Button>
                                <Button size="small" color="error" onClick={() => handleDelete(taxpayer)} startIcon={<Delete />}>
                                  Delete
                                </Button>
                              </TableCell>
                            </TableRow>
                          ))
                        ) : (
                          <TableRow>
                            <TableCell colSpan={19} align="center">
                              <Typography variant="body2" color="textSecondary">
                                No taxpayers found
                              </Typography>
                            </TableCell>
                          </TableRow>
                        )}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </>
          )}
        </Box>
      )}

      {tab === 1 && (
        <Box>
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
              <CircularProgress />
            </Box>
          ) : error ? (
            <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>
          ) : (
            <>
              {/* Search and Actions */}
              <Card sx={{ mb: 3, boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid #e0e0e0' }}>
                <CardContent sx={{ p: 3 }}>
                  <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} md={5}>
                      <TextField
                        fullWidth
                        label="Search Secondary Businesses..."
                        size="small"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        InputProps={{
                          endAdornment: (
                            <InputAdornment position="end">
                              <Search />
                            </InputAdornment>
                          )
                        }}
                      />
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Button variant="outlined" size="small" startIcon={<CloudUpload />}>
                        Import
                      </Button>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Button variant="outlined" size="small" startIcon={<CloudDownload />}>
                        Export
                      </Button>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Button variant="contained" size="small" startIcon={<Add />} onClick={handleAdd}>
                        Add
                      </Button>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>

              {/* Secondary Businesses Table */}
              <Card sx={{ boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid #e0e0e0' }}>
                <CardContent sx={{ p: 3 }}>
                  <TableContainer sx={{ maxHeight: 500 }}>
                    <Table stickyHeader size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 120 }}>GSTIN</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 200 }}>Business Name</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 130 }}>License Number</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 150 }}>Taxpayer Name</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 130 }}>CID/Co. Reg No</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 120 }}>RAMIS TPN</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 100 }}>Status</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 120 }}>Dzongkhag</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 120 }}>Sector</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 130 }}>Sub-Sector</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 150 }}>Business Activity</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 150 }}>Organisation Type</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 100 }}>Frequency</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 120 }}>Reg. Date</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 120 }}>Commencement Date</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 180 }}>Email</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 130 }}>Mobile</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 200 }}>Business Address</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 150 }}>Remarks</TableCell>
                          <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white', minWidth: 100 }}>Actions</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {filteredSecondary.length > 0 ? (
                          filteredSecondary.map((taxpayer) => (
                            <TableRow key={taxpayer.id} hover sx={{ '&:hover': { bgcolor: '#f5f5f5' } }}>
                              <TableCell>{taxpayer.gstin || '-'}</TableCell>
                              <TableCell>{taxpayer.business_name || '-'}</TableCell>
                              <TableCell>{taxpayer.license_number || '-'}</TableCell>
                              <TableCell>{taxpayer.taxpayer_name || '-'}</TableCell>
                              <TableCell>{taxpayer.cid_company_reg_no || '-'}</TableCell>
                              <TableCell>{taxpayer.ramis_tpn || '-'}</TableCell>
                              <TableCell>
                                <Typography sx={{ color: taxpayer.status === 'Active' ? '#2e7d32' : '#d32f2f', fontWeight: 'bold' }}>
                                  {taxpayer.status || '-'}
                                </Typography>
                              </TableCell>
                              <TableCell>{taxpayer.dzongkhag || '-'}</TableCell>
                              <TableCell>{taxpayer.sector || '-'}</TableCell>
                              <TableCell>{taxpayer.sub_sector || '-'}</TableCell>
                              <TableCell>{taxpayer.business_activity || '-'}</TableCell>
                              <TableCell>{taxpayer.organisation_type || '-'}</TableCell>
                              <TableCell>{taxpayer.frequency || '-'}</TableCell>
                              <TableCell>{taxpayer.registration_date || '-'}</TableCell>
                              <TableCell>{taxpayer.commencement_date || '-'}</TableCell>
                              <TableCell>{taxpayer.email_address || '-'}</TableCell>
                              <TableCell>{taxpayer.mobile_number || '-'}</TableCell>
                              <TableCell sx={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{taxpayer.business_address || '-'}</TableCell>
                              <TableCell sx={{ maxWidth: 150, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{taxpayer.remarks || '-'}</TableCell>
                              <TableCell>
                                <Button size="small" onClick={() => handleEdit(taxpayer)} startIcon={<Edit />} sx={{ mr: 1 }}>
                                  Edit
                                </Button>
                                <Button size="small" color="error" onClick={() => handleDelete(taxpayer)} startIcon={<Delete />}>
                                  Delete
                                </Button>
                              </TableCell>
                            </TableRow>
                          ))
                        ) : (
                          <TableRow>
                            <TableCell colSpan={19} align="center">
                              <Typography variant="body2" color="textSecondary">
                                No secondary businesses found
                              </Typography>
                            </TableCell>
                          </TableRow>
                        )}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </>
          )}
        </Box>
      )}

      {/* Edit Dialog */}
      <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)} maxWidth="lg" fullWidth PaperProps={{ sx: { borderRadius: 2 } }}>
        <DialogTitle sx={{ bgcolor: '#1a237e', color: 'white', py: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
            {selectedTaxpayer ? 'Edit Taxpayer' : 'Add New Taxpayer'}
          </Typography>
        </DialogTitle>
        <DialogContent sx={{ p: 3 }}>
          <Grid container spacing={4} sx={{ mt: 1 }}>
            {/* Row 1 */}
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="GSTIN" 
                size="small" 
                defaultValue={selectedTaxpayer?.gstin || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Taxpayer Name" 
                size="small" 
                defaultValue={selectedTaxpayer?.taxpayer_name || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Business Name" 
                size="small" 
                defaultValue={selectedTaxpayer?.business_name || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            
            {/* Row 2 */}
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="CID/Co. Reg No" 
                size="small" 
                defaultValue={selectedTaxpayer?.cid_company_reg_no || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="RAMIS TPN" 
                size="small" 
                defaultValue={selectedTaxpayer?.ramis_tpn || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth size="small" sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}>
                <InputLabel>Status</InputLabel>
                <Select label="Status" defaultValue={selectedTaxpayer?.status || 'Active'}>
                  <MenuItem value="Active">Active</MenuItem>
                  <MenuItem value="Inactive">Inactive</MenuItem>
                  <MenuItem value="Suspended">Suspended</MenuItem>
                  <MenuItem value="Cancelled">Cancelled</MenuItem>
                  <MenuItem value="Deregistered">Deregistered</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            {/* Row 3 */}
            <Grid item xs={12} md={4}>
              <FormControl fullWidth size="small" sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}>
                <InputLabel>Dzongkhag</InputLabel>
                <Select label="Dzongkhag" defaultValue={selectedTaxpayer?.dzongkhag || 'Mongar'}>
                  <MenuItem value="Mongar">Mongar</MenuItem>
                  <MenuItem value="Trashigang">Trashigang</MenuItem>
                  <MenuItem value="Trashiyangtse">Trashiyangtse</MenuItem>
                  <MenuItem value="Lhuentse">Lhuentse</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Sector" 
                size="small" 
                defaultValue={selectedTaxpayer?.sector || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Sub-Sector" 
                size="small" 
                defaultValue={selectedTaxpayer?.sub_sector || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            
            {/* Row 4 */}
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Business Activity" 
                size="small" 
                defaultValue={selectedTaxpayer?.business_activity || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth size="small" sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}>
                <InputLabel shrink>Organization Type</InputLabel>
                <Select label="Organization Type" defaultValue={selectedTaxpayer?.organisation_type || ''}>
                  <MenuItem value="Sole Proprietorship">Sole Proprietorship</MenuItem>
                  <MenuItem value="Private Company">Private Company</MenuItem>
                  <MenuItem value="Public Company">Public Company</MenuItem>
                  <MenuItem value="Partnership">Partnership</MenuItem>
                  <MenuItem value="Government Entity">Government Entity</MenuItem>
                  <MenuItem value="Foreign Company">Foreign Company</MenuItem>
                  <MenuItem value="Joint Venture">Joint Venture</MenuItem>
                  <MenuItem value="State Owned Company">State Owned Company</MenuItem>
                  <MenuItem value="Other">Other</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth size="small" sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}>
                <InputLabel>Frequency</InputLabel>
                <Select label="Frequency" defaultValue={selectedTaxpayer?.frequency || 'Monthly'}>
                  <MenuItem value="Monthly">Monthly</MenuItem>
                  <MenuItem value="Quarterly">Quarterly</MenuItem>
                  <MenuItem value="Half Yearly">Half Yearly</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            {/* Row 5 */}
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Registration Date" 
                size="small" 
                type="date" 
                InputLabelProps={{ shrink: true }} 
                defaultValue={selectedTaxpayer?.registration_date || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Commencement Date" 
                size="small" 
                type="date" 
                InputLabelProps={{ shrink: true }} 
                defaultValue={selectedTaxpayer?.commencement_date || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Deregistration Date" 
                size="small" 
                type="date" 
                InputLabelProps={{ shrink: true }} 
                defaultValue={selectedTaxpayer?.deregistration_date || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            
            {/* Row 6 */}
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Email Address" 
                size="small" 
                defaultValue={selectedTaxpayer?.email_address || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Mobile Number" 
                size="small" 
                defaultValue={selectedTaxpayer?.mobile_number || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Business Address" 
                size="small" 
                defaultValue={selectedTaxpayer?.business_address || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            
            {/* Row 7 */}
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="License Number" 
                size="small" 
                defaultValue={selectedTaxpayer?.license_number || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              {/* Empty */}
            </Grid>
            <Grid item xs={12} md={4}>
              {/* Empty */}
            </Grid>
            
            {/* Row 8 - Remarks (100% width) */}
            <Grid item xs={12}>
              <TextField 
                fullWidth 
                label="Remarks" 
                size="small" 
                multiline 
                rows={2} 
                defaultValue={selectedTaxpayer?.remarks || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1 }, '& .MuiInputBase-input': { textAlign: 'right' } }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions sx={{ p: 3, bgcolor: '#f5f5f5' }}>
          <Button onClick={() => setEditDialogOpen(false)} sx={{ borderRadius: 1 }}>Cancel</Button>
          <Button variant="contained" onClick={() => setEditDialogOpen(false)} sx={{ borderRadius: 1, bgcolor: '#1a237e', '&:hover': { bgcolor: '#303f9f' } }}>
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)} maxWidth="sm" PaperProps={{ sx: { borderRadius: 2 } }}>
        <DialogTitle sx={{ bgcolor: '#d32f2f', color: 'white', py: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
            Confirm Delete
          </Typography>
        </DialogTitle>
        <DialogContent sx={{ p: 3 }}>
          <Typography variant="body1" sx={{ color: '#424242' }}>
            Are you sure you want to delete this taxpayer? This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions sx={{ p: 3, bgcolor: '#f5f5f5' }}>
          <Button onClick={() => setDeleteDialogOpen(false)} sx={{ borderRadius: 1 }}>Cancel</Button>
          <Button color="error" variant="contained" onClick={() => setDeleteDialogOpen(false)} sx={{ borderRadius: 1 }}>
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default Registration
