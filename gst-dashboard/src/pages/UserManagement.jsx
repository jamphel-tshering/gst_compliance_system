import { Box, Typography, Card, CardContent, TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material'

const UserManagement = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        User Management
      </Typography>
      <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
        Manage GST officer accounts and roles. Invite new officers to the portal.
      </Typography>
      
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Invite Officer
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
            Send an invitation for a new GST officer account.
          </Typography>
          
          <TextField
            fullWidth
            label="Officer Email"
            placeholder="officer@rgob.gov.bt"
            size="small"
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Role"
            select
            size="small"
            defaultValue="Officer (User)"
            sx={{ mb: 2 }}
          >
            <MenuItem value="Officer (User)">Officer (User)</MenuItem>
            <MenuItem value="Admin">Admin</MenuItem>
            <MenuItem value="Supervisor">Supervisor</MenuItem>
          </TextField>
          <Button variant="contained">Send Invitation</Button>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Portal Users
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
            1 registered officer account(s).
          </Typography>
          
          <TableContainer component={Paper} sx={{ mt: 2 }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell>Role</TableCell>
                  <TableCell>Joined</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow>
                  <TableCell>Jamphel Tshering</TableCell>
                  <TableCell>jimmes2008@gmail.com</TableCell>
                  <TableCell>admin</TableCell>
                  <TableCell>8/9/2026</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  )
}

export default UserManagement