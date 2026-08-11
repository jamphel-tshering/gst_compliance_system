import { useState } from 'react'
import { Box, Typography, Card, CardContent, Grid, TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Dialog, DialogTitle, DialogContent, DialogActions, FormControl, InputLabel, Select, MenuItem, InputAdornment } from '@mui/material'
import { Search, Add, Edit, Delete, CloudUpload, CloudDownload } from '@mui/icons-material'

const GSTReturns = () => {
  const [searchTerm, setSearchTerm] = useState('')
  const [editDialogOpen, setEditDialogOpen] = useState(false)
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
  const [selectedReturn, setSelectedReturn] = useState(null)

  const [returns, setReturns] = useState([
    { id: 1, gstin: 'C10059014', taxpayerName: 'RIGSAR-PES JOINT VENTURE', taxPeriod: '2026-05-01', filingStatus: 'Filed', paymentStatus: 'Paid', gstPayable: 45000 },
    { id: 2, gstin: 'P10067996', taxpayerName: 'Gyem Phuntsho', taxPeriod: '2026-05-01', filingStatus: 'Not Filed', paymentStatus: 'Not Paid', gstPayable: 12000 },
  ])

  const handleEdit = (ret) => {
    setSelectedReturn(ret)
    setEditDialogOpen(true)
  }

  const handleDelete = (ret) => {
    setSelectedReturn(ret)
    setDeleteDialogOpen(true)
  }

  const handleAdd = () => {
    setSelectedReturn(null)
    setEditDialogOpen(true)
  }

  const filteredReturns = returns.filter(r => 
    r.gstin.toLowerCase().includes(searchTerm.toLowerCase()) ||
    r.taxpayerName.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <Box sx={{ p: 4, bgcolor: '#fafafa', minHeight: '100vh' }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" gutterBottom sx={{ fontWeight: 700, color: '#1a237e', mb: 1 }}>
          GST Returns
        </Typography>
        <Typography variant="body1" color="#616161" sx={{ fontSize: '1rem' }}>
          Track and manage GST return filings, payments, and compliance status
        </Typography>
      </Box>

      {/* Search and Actions */}
      <Card sx={{ mb: 3, boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid #e0e0e0' }}>
        <CardContent sx={{ p: 3 }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={5}>
              <TextField
                fullWidth
                label="Search Returns..."
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

      {/* Returns Table */}
      <Card sx={{ boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid #e0e0e0' }}>
        <CardContent sx={{ p: 3 }}>
          <TableContainer sx={{ maxHeight: 500 }}>
            <Table stickyHeader size="small">
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>GSTIN</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Taxpayer Name</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Tax Period</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Filing Status</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Payment Status</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>GST Payable</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredReturns.map((ret) => (
                  <TableRow key={ret.id} hover sx={{ '&:hover': { bgcolor: '#f5f5f5' } }}>
                    <TableCell>{ret.gstin}</TableCell>
                    <TableCell>{ret.taxpayerName}</TableCell>
                    <TableCell>{ret.taxPeriod}</TableCell>
                    <TableCell>
                      <Typography sx={{ color: ret.filingStatus === 'Filed' ? '#2e7d32' : '#d32f2f' }}>
                        {ret.filingStatus}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography sx={{ color: ret.paymentStatus === 'Paid' ? '#2e7d32' : '#ed6c02' }}>
                        {ret.paymentStatus}
                      </Typography>
                    </TableCell>
                    <TableCell>Nu {ret.gstPayable.toLocaleString()}</TableCell>
                    <TableCell>
                      <Button size="small" onClick={() => handleEdit(ret)} startIcon={<Edit />} sx={{ mr: 1 }}>
                        Edit
                      </Button>
                      <Button size="small" color="error" onClick={() => handleDelete(ret)} startIcon={<Delete />}>
                        Delete
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Edit Dialog */}
      <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)} maxWidth="md" fullWidth PaperProps={{ sx: { borderRadius: 2 } }}>
        <DialogTitle sx={{ bgcolor: '#1a237e', color: 'white', py: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
            {selectedReturn ? 'Edit Return' : 'Add New Return'}
          </Typography>
        </DialogTitle>
        <DialogContent sx={{ p: 3 }}>
          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <Typography variant="subtitle2" sx={{ color: '#1a237e', fontWeight: 'bold', mb: 2, textTransform: 'uppercase', fontSize: '0.75rem' }}>
                Taxpayer Information
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField 
                fullWidth 
                label="GSTIN" 
                size="small" 
                defaultValue={selectedReturn?.gstin || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField 
                fullWidth 
                label="Taxpayer Name" 
                size="small" 
                defaultValue={selectedReturn?.taxpayerName || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="subtitle2" sx={{ color: '#1a237e', fontWeight: 'bold', mb: 2, mt: 2, textTransform: 'uppercase', fontSize: '0.75rem' }}>
                Return Details
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField 
                fullWidth 
                label="Tax Period" 
                size="small" 
                type="date" 
                InputLabelProps={{ shrink: true }} 
                defaultValue={selectedReturn?.taxPeriod || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth size="small" sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}>
                <InputLabel>Filing Status</InputLabel>
                <Select label="Filing Status" defaultValue={selectedReturn?.filingStatus || 'Not Filed'}>
                  <MenuItem value="Filed">Filed</MenuItem>
                  <MenuItem value="Not Filed">Not Filed</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth size="small" sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}>
                <InputLabel>Payment Status</InputLabel>
                <Select label="Payment Status" defaultValue={selectedReturn?.paymentStatus || 'Not Paid'}>
                  <MenuItem value="Paid">Paid</MenuItem>
                  <MenuItem value="Not Paid">Not Paid</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField 
                fullWidth 
                label="GST Payable" 
                size="small" 
                type="number" 
                defaultValue={selectedReturn?.gstPayable || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
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
            Are you sure you want to delete this return? This action cannot be undone.
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

export default GSTReturns
