import { useState } from 'react'
import { Box, Typography, Card, CardContent, Grid, TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Dialog, DialogTitle, DialogContent, DialogActions, FormControl, InputLabel, Select, MenuItem, InputAdornment } from '@mui/material'
import { Search, Add, CloudDownload, Edit, Delete } from '@mui/icons-material'

const TaxpayerEnquiry = () => {
  const [searchTerm, setSearchTerm] = useState('')
  const [editDialogOpen, setEditDialogOpen] = useState(false)
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
  const [selectedEnquiry, setSelectedEnquiry] = useState(null)

  const enquiryTypes = [
    'Taxpayer Enquiry',
    'Official Correspondence',
    'Clarification',
    'Notice',
    'Assessment',
    'Audit',
    'Refund',
    'ITC',
    'Registration',
    'Payment',
    'Return Filing',
    'Other'
  ]

  const modes = [
    'Letter',
    'Email',
    'Phone',
    'In Person',
    'BITs',
    'Official Letter',
    'Other'
  ]

  const statuses = [
    'Open',
    'Pending Taxpayer',
    'Pending Officer',
    'Referred',
    'Resolved',
    'Closed'
  ]

  const [enquiries, setEnquiries] = useState([
    { 
      id: 1, 
      date: '2024-08-26',
      gstin: 'C10059014', 
      taxpayerName: 'RIGSAR-PES JOINT VENTURE', 
      enquiryType: 'Taxpayer Enquiry',
      subject: 'Filing status clarification',
      receivedFrom: 'John Doe',
      mode: 'Email',
      referenceNo: 'REF-001',
      actionResponse: 'Pending',
      status: 'Open',
      responsibleOfficer: 'Officer A',
      dueDate: '2024-09-01',
      closureDate: '',
      remarks: 'Urgent',
      documentLink: ''
    },
    { 
      id: 2, 
      date: '2024-08-25',
      gstin: 'P10067996', 
      taxpayerName: 'Gyem Phuntsho', 
      enquiryType: 'Payment Query',
      subject: 'Payment discrepancy',
      receivedFrom: 'Jane Smith',
      mode: 'Phone',
      referenceNo: 'REF-002',
      actionResponse: 'Resolved',
      status: 'Closed',
      responsibleOfficer: 'Officer B',
      dueDate: '2024-08-28',
      closureDate: '2024-08-28',
      remarks: 'Payment verified',
      documentLink: ''
    },
  ])

  const handleEdit = (enquiry) => {
    setSelectedEnquiry(enquiry)
    setEditDialogOpen(true)
  }

  const handleDelete = (enquiry) => {
    setSelectedEnquiry(enquiry)
    setDeleteDialogOpen(true)
  }

  const handleAdd = () => {
    setSelectedEnquiry(null)
    setEditDialogOpen(true)
  }

  const filteredEnquiries = enquiries.filter(e => 
    e.gstin.toLowerCase().includes(searchTerm.toLowerCase()) ||
    e.taxpayerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    e.enquiryType.toLowerCase().includes(searchTerm.toLowerCase()) ||
    e.subject.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const getStatusColor = (status) => {
    switch(status) {
      case 'Open': return 'orange'
      case 'Pending Taxpayer': return 'orange'
      case 'Pending Officer': return 'orange'
      case 'Referred': return 'purple'
      case 'Resolved': return 'green'
      case 'Closed': return 'gray'
      default: return 'black'
    }
  }

  return (
    <Box sx={{ p: 4, bgcolor: '#fafafa', minHeight: '100vh' }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" gutterBottom sx={{ fontWeight: 700, color: '#1a237e', mb: 1 }}>
          Taxpayer Enquiry
        </Typography>
        <Typography variant="body1" color="#616161" sx={{ fontSize: '1rem' }}>
          Search and manage taxpayer enquiries and responses
        </Typography>
      </Box>

      {/* Search and Actions */}
      <Card sx={{ mb: 3, boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid #e0e0e0' }}>
        <CardContent sx={{ p: 3 }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={5}>
              <TextField
                fullWidth
                label="Search Enquiries..."
                size="small"
                placeholder="Search by GSTIN, name, enquiry type, or subject"
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
              <Button variant="contained" size="small" startIcon={<Add />} onClick={handleAdd}>
                Add Enquiry
              </Button>
            </Grid>
            <Grid item xs={6} md={2}>
              <Button variant="outlined" size="small" startIcon={<CloudDownload />}>
                Export
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Enquiries Table */}
      <Card sx={{ boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid #e0e0e0' }}>
        <CardContent sx={{ p: 3 }}>
          <TableContainer sx={{ maxHeight: 600 }}>
            <Table stickyHeader size="small">
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Enquiry ID</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Date</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>GSTIN</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Taxpayer Name</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Enquiry Type</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Subject / Issue</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Received From / Sent To</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Mode</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Reference No.</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Action / Response</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Status</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Responsible Officer</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Due Date</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Closure Date</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Remarks</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Document Link</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', bgcolor: '#1a237e', color: 'white' }}>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredEnquiries.length > 0 ? (
                  filteredEnquiries.map((enquiry) => (
                    <TableRow key={enquiry.id} hover sx={{ '&:hover': { bgcolor: '#f5f5f5' } }}>
                      <TableCell>{enquiry.id}</TableCell>
                      <TableCell>{enquiry.date}</TableCell>
                      <TableCell>{enquiry.gstin}</TableCell>
                      <TableCell>{enquiry.taxpayerName}</TableCell>
                      <TableCell>{enquiry.enquiryType}</TableCell>
                      <TableCell>{enquiry.subject}</TableCell>
                      <TableCell>{enquiry.receivedFrom}</TableCell>
                      <TableCell>{enquiry.mode}</TableCell>
                      <TableCell>{enquiry.referenceNo}</TableCell>
                      <TableCell>{enquiry.actionResponse}</TableCell>
                      <TableCell>
                        <Typography sx={{ 
                          color: getStatusColor(enquiry.status),
                          fontWeight: 'bold',
                          fontSize: '0.8rem'
                        }}>
                          {enquiry.status}
                        </Typography>
                      </TableCell>
                      <TableCell>{enquiry.responsibleOfficer}</TableCell>
                      <TableCell>{enquiry.dueDate}</TableCell>
                      <TableCell>{enquiry.closureDate || '-'}</TableCell>
                      <TableCell>{enquiry.remarks}</TableCell>
                      <TableCell>{enquiry.documentLink || '-'}</TableCell>
                      <TableCell>
                        <Button size="small" onClick={() => handleEdit(enquiry)} startIcon={<Edit />} sx={{ mr: 1 }}>
                          Edit
                        </Button>
                        <Button size="small" color="error" onClick={() => handleDelete(enquiry)} startIcon={<Delete />}>
                          Delete
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={18} align="center">
                      <Typography variant="body2" color="textSecondary">
                        No enquiries found. Click "Add Enquiry" to create one.
                      </Typography>
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Edit/Add Dialog */}
      <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)} maxWidth="lg" fullWidth PaperProps={{ sx: { borderRadius: 2 } }}>
        <DialogTitle sx={{ bgcolor: '#1a237e', color: 'white', py: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
            {selectedEnquiry ? 'Edit Enquiry' : 'Add New Enquiry'}
          </Typography>
        </DialogTitle>
        <DialogContent sx={{ p: 3 }}>
          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <Typography variant="subtitle2" sx={{ color: '#1a237e', fontWeight: 'bold', mb: 2, textTransform: 'uppercase', fontSize: '0.75rem' }}>
                Enquiry Details
              </Typography>
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField 
                fullWidth 
                label="Date" 
                size="small" 
                type="date" 
                InputLabelProps={{ shrink: true }} 
                defaultValue={selectedEnquiry?.date || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField 
                fullWidth 
                label="GSTIN" 
                size="small" 
                defaultValue={selectedEnquiry?.gstin || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField 
                fullWidth 
                label="Taxpayer Name" 
                size="small" 
                defaultValue={selectedEnquiry?.taxpayerName || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth size="small" sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}>
                <InputLabel>Enquiry Type</InputLabel>
                <Select label="Enquiry Type" defaultValue={selectedEnquiry?.enquiryType || ''}>
                  {enquiryTypes.map((type) => (
                    <MenuItem key={type} value={type}>{type}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={8}>
              <TextField 
                fullWidth 
                label="Subject / Issue" 
                size="small" 
                defaultValue={selectedEnquiry?.subject || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="subtitle2" sx={{ color: '#1a237e', fontWeight: 'bold', mb: 2, mt: 2, textTransform: 'uppercase', fontSize: '0.75rem' }}>
                Communication Details
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Received From / Sent To" 
                size="small" 
                defaultValue={selectedEnquiry?.receivedFrom || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth size="small" sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}>
                <InputLabel>Mode</InputLabel>
                <Select label="Mode" defaultValue={selectedEnquiry?.mode || ''}>
                  {modes.map((mode) => (
                    <MenuItem key={mode} value={mode}>{mode}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Reference No." 
                size="small" 
                defaultValue={selectedEnquiry?.referenceNo || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField 
                fullWidth 
                label="Action / Response" 
                size="small" 
                multiline 
                rows={3} 
                defaultValue={selectedEnquiry?.actionResponse || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1 } }}
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="subtitle2" sx={{ color: '#1a237e', fontWeight: 'bold', mb: 2, mt: 2, textTransform: 'uppercase', fontSize: '0.75rem' }}>
                Status & Assignment
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth size="small" sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}>
                <InputLabel>Status</InputLabel>
                <Select label="Status" defaultValue={selectedEnquiry?.status || 'Open'}>
                  {statuses.map((status) => (
                    <MenuItem key={status} value={status}>{status}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Responsible Officer" 
                size="small" 
                defaultValue={selectedEnquiry?.responsibleOfficer || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Due Date" 
                size="small" 
                type="date" 
                InputLabelProps={{ shrink: true }} 
                defaultValue={selectedEnquiry?.dueDate || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField 
                fullWidth 
                label="Closure Date" 
                size="small" 
                type="date" 
                InputLabelProps={{ shrink: true }} 
                defaultValue={selectedEnquiry?.closureDate || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
              />
            </Grid>
            <Grid item xs={12} md={8}>
              <TextField 
                fullWidth 
                label="Document Link" 
                size="small" 
                defaultValue={selectedEnquiry?.documentLink || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1, height: '40px' } }}
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="subtitle2" sx={{ color: '#1a237e', fontWeight: 'bold', mb: 2, mt: 2, textTransform: 'uppercase', fontSize: '0.75rem' }}>
                Additional Information
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <TextField 
                fullWidth 
                label="Remarks" 
                size="small" 
                multiline 
                rows={2} 
                defaultValue={selectedEnquiry?.remarks || ''} 
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 1 } }}
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
            Are you sure you want to delete this enquiry? This action cannot be undone.
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

export default TaxpayerEnquiry
